import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
import json
import os
import datetime
import time
import warnings

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.dense_retriever import DenseRetriever
from src.retrieval.rrf import RRFFuser
from src.retrieval.reranker import Reranker
from src.generation.generator import AnswerGenerator
from src.generation.citation_verifier import CitationVerifier

from src.embeddings.embedder import LocalEmbedder
import re

_embedder = None

def calculate_similarity(expected, generated):
    global _embedder
    if not expected or not generated:
        return 0.0
        
    # Strip citations and boilerplate
    generated_clean = re.sub(r'\[.*?\]', '', generated)
    if "WHAT I COULD NOT VERIFY:" in generated_clean:
        generated_clean = generated_clean.split("WHAT I COULD NOT VERIFY:")[0]
    generated_clean = generated_clean.strip()
    
    if _embedder is None:
        _embedder = LocalEmbedder()
        
    try:
        expected_vec = _embedder.embed_query(expected)
        generated_vec = _embedder.embed_query(generated_clean)
        return float(cosine_similarity([expected_vec], [generated_vec])[0][0])
    except Exception:
        return 0.0

def calculate_refusal(answerable, generated_answer):
    if answerable:
        return 'N/A'
    
    return 1 if 'NO_ANSWER_FOUND' in generated_answer else 0

def calculate_retrieval_metrics(retrieved_chunk_ids, expected_chunk_ids):
    if not expected_chunk_ids:
        return None
    
    metrics = {}
    
    # Hit@K
    for k in [1, 3, 5, 10]:
        top_k_ids = retrieved_chunk_ids[:k]
        hit = 1 if any(chunk_id in top_k_ids for chunk_id in expected_chunk_ids) else 0
        metrics[f'Hit@{k}'] = hit
        
    # Recall@K
    num_expected = len(expected_chunk_ids)
    for k in [5, 10]:
        top_k_ids = retrieved_chunk_ids[:k]
        recall = sum(1 for chunk_id in expected_chunk_ids if chunk_id in top_k_ids) / num_expected
        metrics[f'Recall@{k}'] = recall
        
    # MRR and First relevant rank
    mrr = 0.0
    first_relevant_rank = None
    for i, chunk_id in enumerate(retrieved_chunk_ids):
        if chunk_id in expected_chunk_ids:
            first_relevant_rank = i + 1
            mrr = 1.0 / first_relevant_rank
            break
            
    metrics['MRR'] = mrr
    metrics['First relevant rank'] = first_relevant_rank
    
    return metrics

def run_evaluation(strategy):
    print(f'Starting evaluation with strategy: {strategy}')
    
    dataset_path = 'data/evaluation/golden_dataset.json'
    if not os.path.exists(dataset_path):
        print(f'Dataset not found at {dataset_path}')
        return []
        
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    dense_retriever = DenseRetriever() if strategy in ['dense', 'hybrid'] else None
    bm25_retriever = BM25Retriever() if strategy == 'hybrid' else None
    rrf = RRFFuser(k=60, dense_weight=1.0, bm25_weight=1.0) if strategy == 'hybrid' else None
    reranker = Reranker() if strategy == 'hybrid' else None
    generator = AnswerGenerator()
    verifier = CitationVerifier()
    
    results = []
    failed_questions = []
    
    for item in dataset:
        qid = item.get('id')
        question = item.get('question')
        expected_answer = item.get('expected_answer', '')
        expected_chunks = item.get('relevant_chunks', [])
        answerable = 'expected_answer' in item
        
        try:
            if strategy == 'dense':
                retrieved_results = dense_retriever.search(query=question, top_k=10)
            elif strategy == 'hybrid':
                d_res = dense_retriever.search(query=question, top_k=20)
                b_res = bm25_retriever.search(query=question, top_k=20)
                fused = rrf.fuse(dense_results=d_res, bm25_results=b_res, top_k=20)
                retrieved_results = reranker.rerank(query=question, results=fused, top_k=10)
                
            retrieved_doc_ids = [r['document_id'] for r in retrieved_results]
            
            answer = generator.generate(question=question, chunks=retrieved_results)
            
            try:
                citation_result = verifier.verify(answer=answer, chunks=retrieved_results)
                citation_support_rate = citation_result.get('citation_support_rate', 0.0)
            except Exception as e:
                print(f"Citation verification failed for {qid}: {e}")
                citation_support_rate = 0.0
                
            retrieval_metrics = calculate_retrieval_metrics(retrieved_doc_ids, expected_chunks)
            sim_score = calculate_similarity(expected_answer, answer)
            refusal_score = calculate_refusal(answerable, answer)
            
            res_item = {
                'id': qid,
                'question': question,
                'answerable': answerable,
                'expected_answer': expected_answer,
                'generated_answer': answer,
                'expected_chunks': expected_chunks,
                'retrieved_chunks': retrieved_doc_ids,
                'reference_answer_similarity': sim_score,
                'citation_support_rate': citation_support_rate,
                'refusal_correctness': refusal_score
            }
            if retrieval_metrics:
                res_item.update(retrieval_metrics)
                
            results.append(res_item)
            
            # Add delay to avoid rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f'Error evaluating {qid}: {e}')
            failed_questions.append(qid)
            
    print(f'Questions successful: {len(results)}')
    print(f'Questions failed: {len(failed_questions)}')
    if failed_questions:
        print(f'Failed question IDs: {", ".join(failed_questions)}')
        
    return results

def aggregate_metrics(results):
    if not results:
        return {}
        
    total = len(results)
    answerable_count = sum(1 for r in results if r['answerable'])
    unanswerable_count = total - answerable_count
    
    agg = {
        'Questions evaluated': total,
        'Answerable questions': answerable_count,
        'Unanswerable questions': unanswerable_count
    }
    
    retrieval_keys = ['Hit@1', 'Hit@3', 'Hit@5', 'Hit@10', 'Recall@5', 'Recall@10', 'MRR']
    for k in retrieval_keys:
        valid_vals = [r[k] for r in results if k in r]
        agg[k] = sum(valid_vals) / len(valid_vals) if valid_vals else 0.0
        
    valid_sims = [r['reference_answer_similarity'] for r in results if r['answerable']]
    agg['Reference Answer Similarity'] = sum(valid_sims) / len(valid_sims) if valid_sims else 0.0
    
    valid_cits = [r['citation_support_rate'] for r in results if r['answerable']]
    agg['Citation Support Rate'] = sum(valid_cits) / len(valid_cits) if valid_cits else 0.0
    
    valid_refusals = [r['refusal_correctness'] for r in results if r['refusal_correctness'] != 'N/A']
    agg['Refusal Correctness'] = sum(valid_refusals) / len(valid_refusals) if valid_refusals else 0.0
    
    return agg

def print_summary(strategy, agg):
    print(f'\n============================================================')
    print(f'RAG EVALUATION SUMMARY')
    print(f'============================================================')
    print(f'Strategy: {strategy.upper()}')
    print(f'Questions evaluated: {agg.get("Questions evaluated", 0)}')
    print(f'Answerable questions: {agg.get("Answerable questions", 0)}')
    print(f'Unanswerable questions: {agg.get("Unanswerable questions", 0)}')
    print(f'\nRETRIEVAL')
    print(f'------------------------------------------------------------')
    print(f'Hit@1:       {agg.get("Hit@1", 0):.2%}')
    print(f'Hit@3:       {agg.get("Hit@3", 0):.2%}')
    print(f'Hit@5:       {agg.get("Hit@5", 0):.2%}')
    print(f'Hit@10:      {agg.get("Hit@10", 0):.2%}')
    print(f'Recall@5:    {agg.get("Recall@5", 0):.2%}')
    print(f'Recall@10:   {agg.get("Recall@10", 0):.2%}')
    print(f'MRR:         {agg.get("MRR", 0):.2f}')
    print(f'\nANSWER')
    print(f'------------------------------------------------------------')
    print(f'Reference Answer Similarity: {agg.get("Reference Answer Similarity", 0):.2%}')
    print(f'\nCITATIONS')
    print(f'------------------------------------------------------------')
    print(f'Citation Support Rate: {agg.get("Citation Support Rate", 0):.2%}')
    print(f'\nREFUSAL')
    print(f'------------------------------------------------------------')
    print(f'Correct Refusal Rate: {agg.get("Refusal Correctness", 0):.2%}')
    print(f'============================================================\n')

def generate_markdown_report(strategy_results, agg_results):
    os.makedirs('reports', exist_ok=True)
    report_path = 'reports/evaluation_report.md'
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('# RAG Evaluation Report\n\n')
        f.write('## Evaluation Overview\n\n')
        
        first_strat = list(strategy_results.keys())[0]
        total = agg_results[first_strat].get('Questions evaluated', 0)
        
        f.write(f'- **Number of questions**: {total}\n')
        f.write(f'- **Date/time**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.write(f'- **Strategy**: {", ".join([s.upper() for s in strategy_results.keys()])}\n\n')
        
        f.write('## Overall Metrics\n\n')
        f.write('| Metric | ' + ' | '.join([s.upper() for s in strategy_results.keys()]) + ' |\n')
        f.write('|---|' + '|'.join(['---' for _ in strategy_results.keys()]) + '|\n')
        
        metrics_list = ['Hit@1', 'Hit@3', 'Hit@5', 'Hit@10', 'Recall@5', 'Recall@10', 'MRR', 
                        'Reference Answer Similarity', 'Citation Support Rate', 'Refusal Correctness']
        
        for m in metrics_list:
            row = f'| {m} | '
            for s in strategy_results.keys():
                val = agg_results[s].get(m, 0)
                if m == 'MRR':
                    row += f'{val:.2f} | '
                else:
                    row += f'{val:.2%} | '
            f.write(row + '\n')
            
        f.write('\n## Question Results\n\n')
        
        # Output details for the first strategy by default in the detailed view
        main_results = strategy_results[first_strat]
        for r in main_results:
            f.write(f'### {r.get("id")}\n\n')
            f.write(f'**Question**:\n{r.get("question")}\n\n')
            f.write(f'**Question type**:\n{r.get("question_type")}\n\n')
            f.write(f'**Expected answer**:\n{r.get("expected_answer")}\n\n')
            f.write(f'**Generated answer**:\n{r.get("generated_answer")}\n\n')
            f.write(f'**Expected chunks**:\n{r.get("expected_chunks")}\n\n')
            f.write(f'**Retrieved chunks**:\n{r.get("retrieved_chunks")}\n\n')
            f.write(f'**Retrieval metrics**:\nHit@1: {r.get("Hit@1", 0)}, Hit@5: {r.get("Hit@5", 0)}, Recall@5: {r.get("Recall@5", 0):.2f}, MRR: {r.get("MRR", 0):.2f}\n\n')
            f.write(f'**Reference answer similarity**: {r.get("reference_answer_similarity", 0):.2%}\n\n')
            f.write(f'**Citation support rate**: {r.get("citation_support_rate", 0):.2%}\n\n')
            f.write(f'**Refusal correctness**: {r.get("refusal_correctness", "N/A")}\n\n')
            
            # Failures
            if r.get('answerable', True):
                if r.get('Hit@5', 1) == 0:
                    f.write('❌ Retrieval failure\n')
                if r.get('reference_answer_similarity', 1) < 0.5:
                    f.write('❌ Low answer similarity\n')
                if r.get('citation_support_rate', 1) < 1.0:
                    f.write('❌ Unsupported citation\n')
            
            if r.get('refusal_correctness') == 0:
                f.write('❌ Incorrect refusal\n')
                
            f.write('\n---\n\n')

def main():
    parser = argparse.ArgumentParser(description='Evaluate RAG pipeline')
    parser.add_argument('--strategy', type=str, choices=['dense', 'hybrid', 'both'], default='both', help='Retrieval strategy to evaluate')
    args = parser.parse_args()
    
    strategies_to_run = ['dense', 'hybrid'] if args.strategy == 'both' else [args.strategy]
    
    strategy_results = {}
    agg_results = {}
    
    for s in strategies_to_run:
        results = run_evaluation(s)
        agg = aggregate_metrics(results)
        strategy_results[s] = results
        agg_results[s] = agg
        print_summary(s, agg)
        
    if args.strategy == 'both':
        print(f'------------------------------------------------------------')
        print(f'DENSE vs HYBRID')
        print(f'------------------------------------------------------------')
        print(f'Metric                  Dense       Hybrid')
        print(f'------------------------------------------------------------')
        
        metrics_list = ['Hit@1', 'Hit@3', 'Hit@5', 'Hit@10', 'Recall@5', 'Recall@10', 'MRR', 
                        'Reference Answer Similarity', 'Citation Support Rate', 'Refusal Correctness']
                        
        for m in metrics_list:
            d_val = agg_results['dense'].get(m, 0)
            h_val = agg_results['hybrid'].get(m, 0)
            
            if m == 'MRR':
                print(f'{m:<23} {d_val:<11.2f} {h_val:<11.2f}')
            elif m in ['Reference Answer Similarity', 'Citation Support Rate', 'Refusal Correctness']:
                # Shorten metric name to match requested output slightly
                short_m = m
                if m == 'Reference Answer Similarity': short_m = 'Answer Similarity'
                if m == 'Citation Support Rate': short_m = 'Citation Support'
                
                print(f'{short_m:<23} {d_val:.2%}      {h_val:.2%}')
            else:
                print(f'{m:<23} {d_val:.2%}      {h_val:.2%}')
        
        print(f'------------------------------------------------------------\n')
        
    generate_markdown_report(strategy_results, agg_results)
    
    # Save JSON results
    with open('reports/evaluation_results.json', 'w', encoding='utf-8') as f:
        json.dump({'strategy_results': strategy_results, 'aggregated_metrics': agg_results}, f, indent=2)

if __name__ == '__main__':
    main()

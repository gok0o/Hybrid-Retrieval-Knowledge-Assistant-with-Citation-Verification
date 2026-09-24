import streamlit as st
import json
import os

st.set_page_config(layout='wide', page_title='RAG Evaluation Dashboard')

@st.cache_data
def load_data():
    path = 'reports/evaluation_results.json'
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

st.title('RAG Evaluation Dashboard')

if not data:
    st.error('No evaluation results found. Please run eval.py first.')
    st.stop()

strategies = list(data['strategy_results'].keys())

if 'both' not in strategies and len(strategies) > 1:
    st.sidebar.header('Comparison')
    st.sidebar.write('Both strategies have been run. Comparison mode active.')

strategy = st.sidebar.selectbox('Select Strategy', strategies)

st.header(f'Overall Metrics: {strategy.upper()}')

agg = data['aggregated_metrics'][strategy]

col1, col2, col3, col4 = st.columns(4)
col1.metric('Hit@5', f"{agg.get('Hit@5', 0):.2%}")
col2.metric('MRR', f"{agg.get('MRR', 0):.2f}")
col3.metric('Answer Similarity', f"{agg.get('Reference Answer Similarity', 0):.2%}")
col4.metric('Citation Support', f"{agg.get('Citation Support Rate', 0):.2%}")

if len(strategies) > 1:
    st.subheader('Strategy Comparison')
    
    metrics = ['Hit@1', 'Hit@3', 'Hit@5', 'Hit@10', 'Recall@5', 'Recall@10', 'MRR', 
               'Reference Answer Similarity', 'Citation Support Rate', 'Refusal Correctness']
    
    comp_data = []
    for m in metrics:
        row = {'Metric': m}
        for s in strategies:
            val = data['aggregated_metrics'][s].get(m, 0)
            if m == 'MRR':
                row[s] = f"{val:.2f}"
            else:
                row[s] = f"{val:.2%}"
        comp_data.append(row)
        
    st.dataframe(comp_data)

st.divider()

st.header('Question Results')

results = data['strategy_results'][strategy]
question_options = {r['id']: r['question'] for r in results}
selected_q_id = st.selectbox('Select Question', list(question_options.keys()), format_func=lambda x: f"{x}: {question_options[x][:50]}...")

selected_res = next((r for r in results if r['id'] == selected_q_id), None)

if selected_res:
    st.subheader('Question Details')
    st.write(f"**Question:** {selected_res['question']}")
    st.write(f"**Expected Answer:** {selected_res['expected_answer']}")
    st.write(f"**Generated Answer:** {selected_res['generated_answer']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Expected Chunks:**")
        st.write(selected_res['expected_chunks'])
    with col2:
        st.write("**Retrieved Chunks:**")
        st.write(selected_res['retrieved_chunks'])
        
    st.subheader('Metrics')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Hit@5', selected_res.get('Hit@5', 0))
    col2.metric('MRR', f"{selected_res.get('MRR', 0):.2f}")
    col3.metric('Citation Support Rate', f"{selected_res.get('citation_support_rate', 0):.2%}")
    col4.metric('Refusal Correctness', selected_res.get('refusal_correctness', 'N/A'))


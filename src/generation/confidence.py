class ConfidenceScorer:

    def calculate(
        self,
        reranked_results: list[dict],
        citation_support_rate: float,
        answer: str,
    ) -> dict:

        # -----------------------------------------
        # 1. Retrieval quality
        # -----------------------------------------
        if reranked_results:
            reranker_scores = [
                result["reranker_score"]
                for result in reranked_results
            ]

            # Convert reranker scores into a rough
            # 0-1 confidence value.
            max_score = max(reranker_scores)

            retrieval_score = min(
                max(max_score / 4.0, 0.0),
                1.0,
            )
        else:
            retrieval_score = 0.0

        # -----------------------------------------
        # 2. Citation support
        # -----------------------------------------
        citation_score = citation_support_rate

        # -----------------------------------------
        # 3. Answer completeness
        # -----------------------------------------
        completeness_score = self._calculate_completeness(
            answer
        )

        # -----------------------------------------
        # 4. No-answer detection
        # -----------------------------------------
        no_answer = self._detect_no_answer(answer)

        no_answer_score = 0.0 if no_answer else 1.0

        # -----------------------------------------
        # Final confidence
        # -----------------------------------------
        final_score = (
            0.35 * retrieval_score
            + 0.30 * citation_score
            + 0.20 * completeness_score
            + 0.15 * no_answer_score
        )

        return {
            "overall": round(final_score, 4),
            "retrieval_score": round(
                retrieval_score, 4
            ),
            "citation_support_rate": round(
                citation_score, 4
            ),
            "answer_completeness": round(
                completeness_score, 4
            ),
            "no_answer": no_answer,
        }

    def _calculate_completeness(
        self,
        answer: str,
    ) -> float:

        if not answer:
            return 0.0

        answer_lower = answer.lower()

        # Detect whether the model explicitly says
        # that required information is unavailable.
        missing_phrases = [
            "could not verify",
            "not available",
            "not provided",
            "does not provide",
            "not enough information",
            "cannot be verified",
        ]

        has_missing_information = any(
            phrase in answer_lower
            for phrase in missing_phrases
        )

        # A response that explicitly identifies missing
        # information is considered partially complete.
        if has_missing_information:
            return 0.6

        # Normal answer.
        return 1.0

    def _detect_no_answer(
        self,
        answer: str,
    ) -> bool:

        answer_lower = answer.lower()

        no_answer_phrases = [
            "i could not find",
            "i couldn't find",
            "not enough information",
            "cannot answer",
            "can't answer",
            "could not verify",
        ]

        return any(
            phrase in answer_lower
            for phrase in no_answer_phrases
        )
from typing import Dict

from config.config import TOP_K, SIMILARITY_THRESHOLD


class Retriever:
    def __init__(self, vector_store, embedder, unique_funds=None):
        self.vector_store = vector_store
        self.embedder = embedder
        self.unique_funds = unique_funds or []

    def retrieve(self, query: str) -> Dict:
        """
        Returns a dict:
        {
            "docs": [...],
            "summary": "..."
        }
        """
        query_lower = query.lower()
        query_embedding = self.embedder.embed_texts([query])
        results = self.vector_store.search(query_embedding, TOP_K)

        # Stop words to avoid polluting the summary with "equity", "fund", etc.
        STOP_WORDS = {"equity", "fund", "funds", "total", "what", "is", "the", "for", "number", "holdings", "trades"}
        query_words = [w for w in query_lower.split() if len(w) > 3 and w not in STOP_WORDS]
        
        keyword_results = []
        counts = {} # entity -> count
        
        if hasattr(self.vector_store, "documents"):
            for doc in self.vector_store.documents:
                doc_text_lower = doc["text"].lower()
                
                matched_any = False
                for word in query_words:
                    if word in doc_text_lower:
                        matched_any = True
                        counts[word] = counts.get(word, 0) + 1
                        
                        # Heuristic: check if the doc text mentions holding-only or trade-only fields
                        is_holding = "qty" in doc_text_lower or "mv_base" in doc_text_lower
                        is_trade = "quantity" in doc_text_lower or "allocationid" in doc_text_lower
                        
                        if is_holding:
                            counts[f"{word}_holdings"] = counts.get(f"{word}_holdings", 0) + 1
                        if is_trade:
                            counts[f"{word}_trades"] = counts.get(f"{word}_trades", 0) + 1
                
                if matched_any:
                    keyword_results.append({
                        "text": doc["text"],
                        "metadata": doc["metadata"],
                        "score": 0.9
                    })
        
        # Merge results
        merged = {}
        for r in keyword_results:
            merged[r["text"]] = r
        for r in results:
            if r["text"] not in merged:
                merged[r["text"]] = r
            else:
                merged[r["text"]]["score"] = max(merged[r["text"]]["score"], r["score"])
        
        final_results = sorted(merged.values(), key=lambda x: x["score"], reverse=True)
        final_results = final_results[:TOP_K]

        # Build a summary string if counts exist
        summary_lines = []
        for word in query_words:
            if word in counts:
                total = counts[word]
                holdings_count = counts.get(f"{word}_holdings", 0)
                trades_count = counts.get(f"{word}_trades", 0)
                summary_lines.append(f"Found {total} records matching '{word}' ({holdings_count} in holdings, {trades_count} in trades).")

        # Explicit check for PortfolioNames
        found_funds = []
        for fund in self.unique_funds:
            if fund.lower() in query_lower:
                found_funds.append(fund)
        
        if found_funds:
            summary_lines.append(f"Exact Fund Matches in database: {', '.join(found_funds)}")

        summary = "\n".join(summary_lines)
        if summary:
            print(f"DEBUG SUMMARY:\n{summary}\n")

        if not final_results and not summary:
            return {"docs": [], "summary": ""}

        # Relax threshold if we have keyword summary matches or high scores
        max_score = max((r["score"] for r in final_results), default=0)
        
        # If we have a summary (keyword matches), we are more permissive
        effective_threshold = SIMILARITY_THRESHOLD
        if summary:
            effective_threshold = 0.3 # Significantly more permissive if we found keywords

        if max_score < effective_threshold and not summary:
            return {"docs": [], "summary": ""}

        return {"docs": final_results, "summary": summary}


import re


class MemoryRecallAgent:

    def __init__(self):
        self.memories = []

    def build_memory(self, messages):
        """Store messages as searchable conversation memories."""

        self.memories = []

        for msg in messages:
            text = msg.get("message", "").strip()

            if not text:
                continue

            self.memories.append({
                "sender": msg.get("sender", "Unknown"),
                "timestamp": msg.get("timestamp"),
                "message": text
            })

        return len(self.memories)

    def recall(self, query, limit=5):
        """Find messages relevant to a search query."""

        query_words = set(
            re.findall(r"\b\w+\b", query.lower())
        )

        results = []

        for memory in self.memories:
            message_words = set(
                re.findall(
                    r"\b\w+\b",
                    memory["message"].lower()
                )
            )

            score = len(query_words & message_words)

            if score > 0:
                results.append({
                    **memory,
                    "relevance_score": score
                })

        results.sort(
            key=lambda item: item["relevance_score"],
            reverse=True
        )

        return results[:limit]

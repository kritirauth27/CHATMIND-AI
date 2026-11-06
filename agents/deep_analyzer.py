
from collections import Counter
from datetime import date
import re


class DeepAnalyzerAgent:

    def analyze(self, messages):
        if not messages:
            return {"error": "No messages available"}

        participants = Counter()
        daily_activity = Counter()
        word_frequency = Counter()

        for msg in messages:
            sender = msg.get("sender", "Unknown")
            text = msg.get("message", "")
            timestamp = msg.get("timestamp")

            participants[sender] += 1

            if timestamp:
                daily_activity[str(timestamp.date())] += 1

            words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
            word_frequency.update(words)

        common_words = {
            word: count
            for word, count in word_frequency.most_common(10)
            if word not in {
                "the", "and", "for", "you", "are",
                "that", "this", "with", "have", "was"
            }
        }

        return {
            "total_messages": len(messages),
            "total_participants": len(participants),
            "most_active_participants": participants.most_common(5),
            "daily_activity": dict(daily_activity),
            "frequent_words": common_words,
            "analysis_status": "Completed"
        }

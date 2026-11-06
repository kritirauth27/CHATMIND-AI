
class ReplyGiverAgent:

    def generate_replies(self, messages):
        """Generate context-based reply suggestions."""

        if not messages:
            return ["No conversation available to analyze."]

        latest = messages[-1]
        message = latest.get("message", "").lower()

        suggestions = []

        if any(word in message for word in ["hello", "hi", "hey"]):
            suggestions = [
                "Hey! How are you?",
                "Hello! What's up?",
                "Hi! Good to hear from you."
            ]

        elif any(word in message for word in ["thank", "thanks"]):
            suggestions = [
                "You're welcome!",
                "Happy to help!",
                "No problem at all."
            ]

        elif "?" in message:
            suggestions = [
                "Let me think about that and get back to you.",
                "That's a good question. Can you tell me more?",
                "I'll check and let you know."
            ]

        elif any(word in message for word in ["sorry", "apolog"]):
            suggestions = [
                "It's okay. Thanks for explaining.",
                "I understand.",
                "Let's talk about it calmly."
            ]

        else:
            suggestions = [
                "I understand. Tell me more.",
                "Okay, let's discuss this further.",
                "Thanks for sharing that with me."
            ]

        return {
            "based_on": latest.get("message", ""),
            "sender": latest.get("sender", "Unknown"),
            "suggestions": suggestions,
            "status": "Generated"
        }

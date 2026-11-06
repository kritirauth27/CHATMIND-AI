
from backend.parser import parse_chat
from agents.deep_analyzer import DeepAnalyzerAgent
from agents.memory_recall import MemoryRecallAgent
from agents.reply_giver import ReplyGiverAgent


class ChatMindOrchestrator:

    def __init__(self):
        self.analyzer = DeepAnalyzerAgent()
        self.memory = MemoryRecallAgent()
        self.reply_agent = ReplyGiverAgent()

    def run_pipeline(self, chat_text):

        # Step 1: Parse uploaded chat
        messages = parse_chat(chat_text)

        if not messages:
            return {
                "status": "error",
                "message": "No valid WhatsApp messages found."
            }

        # Step 2: Run Deep Analyzer
        analysis = self.analyzer.analyze(messages)

        # Step 3: Build conversation memory
        memory_count = self.memory.build_memory(messages)

        # Step 4: Generate reply suggestions
        replies = self.reply_agent.generate_replies(messages)

        # Step 5: Combine agent results
        return {
            "status": "success",
            "total_messages": len(messages),
            "analysis": analysis,
            "memory_count": memory_count,
            "reply_suggestions": replies
        }


if __name__ == "__main__":

    sample_chat = """
06/11/26, 10:00 AM - Rahul: Hello
06/11/26, 10:02 AM - Kriti: Hi, how are you?
06/11/26, 10:05 AM - Rahul: Let's discuss our project.
06/11/26, 10:10 AM - Kriti: Sure, let's start.
"""

    system = ChatMindOrchestrator()
    result = system.run_pipeline(sample_chat)

    print("\n===== CHATMIND AI REPORT =====")
    print(result)

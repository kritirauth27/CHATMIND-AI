
import streamlit as st
import pandas as pd
import plotly.express as px

from backend.orchestrator import ChatMindOrchestrator

st.set_page_config(
    page_title="CHATMIND AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 CHATMIND AI")
st.subheader("Autonomous Multi-Agent Chat Intelligence Platform")

st.markdown(
    "Upload a WhatsApp TXT export. "
    "Our agents will automatically analyze the conversation."
)

uploaded_file = st.file_uploader(
    "Upload WhatsApp Chat Export",
    type=["txt"]
)

if uploaded_file is not None:

    chat_text = uploaded_file.getvalue().decode(
        "utf-8-sig",
        errors="replace"
    )

    with st.spinner("Agents are analyzing your conversation..."):

        system = ChatMindOrchestrator()
        result = system.run_pipeline(chat_text)

    if result["status"] == "success":

        analysis = result["analysis"]

        st.success("All agents completed their workflow!")

        st.divider()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Messages",
            result["total_messages"]
        )

        col2.metric(
            "Participants",
            analysis["total_participants"]
        )

        col3.metric(
            "Memories Stored",
            result["memory_count"]
        )

        st.divider()

        st.header("📊 Deep Analyzer Agent")

        participants = analysis["most_active_participants"]

        if participants:
            df = pd.DataFrame(
                participants,
                columns=["Participant", "Messages"]
            )

            fig = px.bar(
                df,
                x="Participant",
                y="Messages",
                title="Participant Activity"
            )

            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Frequently Used Words")

        st.json(analysis["frequent_words"])

        st.divider()

        st.header("🧠 Memory Recall Agent")

        memory_agent = system.memory

        query = st.text_input(
            "Search conversation memories",
            placeholder="Enter a keyword..."
        )

        if query:
            memories = memory_agent.recall(query)

            if memories:
                for item in memories:
                    st.write(
                        f"**{item['sender']}**: "
                        f"{item['message']}"
                    )
                    st.caption(
                        f"Relevance score: "
                        f"{item['relevance_score']}"
                    )
            else:
                st.info("No matching memories found.")

        st.divider()

        st.header("💬 Reply Giver Agent")

        suggestions = result["reply_suggestions"]

        if isinstance(suggestions, dict):
            for index, reply in enumerate(
                suggestions["suggestions"], 1
            ):
                st.write(f"**Suggestion {index}:** {reply}")

        st.divider()

        st.header("⚙️ Agent Execution Report")

        st.write("✅ Deep Analyzer: Completed")
        st.write("✅ Memory Recall: Completed")
        st.write("✅ Reply Giver: Completed")
        st.write("✅ Orchestrator: Completed")

    else:
        st.error(result["message"])

else:
    st.info("Upload a WhatsApp TXT file to begin automatic analysis.")

    st.markdown("""
    ### Our specialized agents

    - 🔍 Deep Analyzer
    - 🧠 Memory Recall
    - 💬 Reply Giver
    - ⚙️ Automatic Orchestrator
    """)

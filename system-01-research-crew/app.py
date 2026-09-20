import streamlit as st

from main import crew, save_report

st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🔎")

st.title("🔎 Multi-Agent Research Assistant")
st.caption(
    "CrewAI + Gemini — 4 collaborating agents: "
    "Research Librarian → Research Analyst → Fact Checker → Technical Writer"
)

topic = st.text_input(
    "Research topic",
    placeholder="e.g. Agentic AI trends in 2026",
)

run_clicked = st.button("Run Research Crew", type="primary", disabled=not topic)

if run_clicked:
    with st.spinner("Agents are researching, analyzing, fact-checking, and writing... this can take a few minutes."):
        try:
            result = crew.kickoff(inputs={"topic": topic})
            report = result.raw if hasattr(result, "raw") else str(result)
            report_path = save_report(topic, report)
        except Exception as error:
            st.error(f"The research crew failed: {error}")
        else:
            st.success(f"Report saved to: {report_path}")
            st.markdown(report)
            st.download_button(
                "Download report (.md)",
                report,
                file_name=report_path.name,
                mime="text/markdown",
            )

import time

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

# The Gemini API occasionally returns an empty/None response for a single
# call (a transient upstream issue, not a bug in this code). Retrying the
# same request a couple of times almost always succeeds.
MAX_ATTEMPTS = 3

if run_clicked:
    status = st.empty()
    last_error = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        status.info(
            f"Agents are researching, analyzing, fact-checking, and writing... "
            f"(attempt {attempt}/{MAX_ATTEMPTS}, this can take a few minutes)"
        )
        try:
            result = crew.kickoff(inputs={"topic": topic})
            report = result.raw if hasattr(result, "raw") else str(result)
            report_path = save_report(topic, report)
        except Exception as error:
            last_error = error
            if attempt < MAX_ATTEMPTS:
                time.sleep(3)
            continue
        else:
            status.empty()
            st.success(f"Report saved to: {report_path}")
            st.markdown(report)
            st.download_button(
                "Download report (.md)",
                report,
                file_name=report_path.name,
                mime="text/markdown",
            )
            break
    else:
        status.empty()
        st.error(
            f"The research crew failed after {MAX_ATTEMPTS} attempts: {last_error}"
        )

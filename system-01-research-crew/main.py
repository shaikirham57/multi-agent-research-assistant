import re
from datetime import datetime
from pathlib import Path

from crewai import Crew, Process

from agents import build_agents
from tasks import build_tasks


# ==================================================
# Create Research Crew
# ==================================================
#
# A fresh Crew (with its own fresh Agent and Task instances) is built
# on every call instead of once at import time. Reusing the same Agent
# objects across multiple runs — e.g. a retry after a failure — can
# trip crewai's "Executor is already running" guard if a previous run's
# internal state wasn't fully cleared. Building fresh objects per run
# avoids that entirely.


def build_crew() -> Crew:
    """Build a brand-new Crew with fresh agents and tasks."""

    searcher, analyst, fact_checker, writer = build_agents()

    search_task, analysis_task, fact_check_task, writing_task = build_tasks(
        searcher, analyst, fact_checker, writer
    )

    return Crew(
        agents=[
            searcher,
            analyst,
            fact_checker,
            writer,
        ],
        tasks=[
            search_task,
            analysis_task,
            fact_check_task,
            writing_task,
        ],
        process=Process.sequential,
        verbose=True,
    )


# ==================================================
# Generate Safe Filename
# ==================================================

def create_safe_filename(topic: str) -> str:
    """Convert the research topic into a safe filename."""

    filename = topic.lower()

    filename = re.sub(
        r"[^a-z0-9]+",
        "_",
        filename
    )

    filename = filename.strip("_")

    return filename


# ==================================================
# Save Report
# ==================================================

def save_report(topic: str, report: str) -> Path:
    """Save the final research report as a Markdown file."""

    project_root = Path(__file__).resolve().parents[1]

    reports_directory = project_root / "reports"

    reports_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    safe_topic = create_safe_filename(topic)

    filename = (
        f"{safe_topic}_{timestamp}.md"
    )

    report_path = reports_directory / filename

    report_path.write_text(
        report,
        encoding="utf-8"
    )

    return report_path


# ==================================================
# Run Research Crew
# ==================================================

if __name__ == "__main__":

    topic = input(
        "\nEnter the research topic: "
    ).strip()

    if not topic:
        print(
            "ERROR: Please enter a research topic."
        )
        raise SystemExit(1)

    print("\n" + "=" * 60)
    print("MULTI-AGENT RESEARCH ASSISTANT")
    print("=" * 60)

    print(f"\nTopic: {topic}")

    print("\nAgents:")
    print("1. Research Librarian")
    print("2. Research Analyst")
    print("3. Fact Checker")
    print("4. Technical Report Writer")

    print("\nPipeline:")
    print(
        "Research → Analysis → Fact Check → Report"
    )

    print("\n" + "=" * 60)
    print("Starting CrewAI execution...")
    print("=" * 60)

    try:

        crew = build_crew()

        result = crew.kickoff(
            inputs={
                "topic": topic
            }
        )

        # ------------------------------------------
        # Extract final report
        # ------------------------------------------

        report = (
            result.raw
            if hasattr(result, "raw")
            else str(result)
        )

        # ------------------------------------------
        # Save report
        # ------------------------------------------

        report_path = save_report(
            topic,
            report
        )

        # ------------------------------------------
        # Display final report
        # ------------------------------------------

        print("\n" + "=" * 60)
        print("FINAL RESEARCH REPORT")
        print("=" * 60)

        print(report)

        print("\n" + "=" * 60)
        print("REPORT SAVED SUCCESSFULLY")
        print("=" * 60)

        print(
            f"\nFile: {report_path}"
        )

        print(
            f"\nLocation: {report_path.parent}"
        )

    except Exception as error:

        print("\n" + "=" * 60)
        print("ERROR")
        print("=" * 60)

        print(
            f"\nThe research crew failed:\n{error}"
        )

        raise

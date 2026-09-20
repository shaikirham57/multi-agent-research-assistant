from crewai import Task


# --------------------------------------------------
# Task factory
# --------------------------------------------------
#
# Tasks are bound to specific agent instances at construction time, so
# a fresh set of tasks must be built for every fresh set of agents
# (see build_agents() in agents.py for why agents are rebuilt per run).


def build_tasks(searcher, analyst, fact_checker, writer):
    """Create a fresh set of the four research tasks for the given agents."""

    # ==================================================
    # Task 1 — Web Research
    # ==================================================

    search_task = Task(
        description=(
            "Research the topic: {topic}\n\n"
            "Use the web_search tool to find 5–8 credible and relevant sources.\n"
            "Prioritize official documentation, research papers, universities, "
            "government organizations, reputable technical organizations, and "
            "first-party sources.\n\n"
            "For every source provide:\n"
            "1. Title\n"
            "2. URL\n"
            "3. Short description\n"
            "4. Why the source is relevant\n\n"
            "Do not invent sources or URLs. Only report sources returned by "
            "the web search tool."
        ),

        expected_output=(
            "A structured research brief containing 5–8 credible sources, "
            "including their titles, URLs, descriptions, and relevance."
        ),

        agent=searcher,
    )

    # ==================================================
    # Task 2 — Research Analysis
    # ==================================================

    analysis_task = Task(
        description=(
            "Analyze the research collected by the Research Librarian.\n\n"
            "Identify 3–5 of the strongest evidence-backed claims about "
            "the topic.\n\n"
            "For each claim provide:\n"
            "1. The claim\n"
            "2. Supporting evidence\n"
            "3. Source URL\n"
            "4. Confidence level\n"
            "5. Any important limitations or uncertainty\n\n"
            "Do not introduce facts that are not supported by the research."
        ),

        expected_output=(
            "A structured analysis containing 3–5 evidence-backed claims "
            "with supporting sources, confidence levels, and uncertainty notes."
        ),

        agent=analyst,

        context=[search_task],
    )

    # ==================================================
    # Task 3 — Fact Checking
    # ==================================================

    fact_check_task = Task(
        description=(
            "Fact-check the research analysis against the collected sources.\n\n"
            "For each major claim:\n"
            "1. Determine whether the claim is supported.\n"
            "2. Check whether the cited source actually supports it.\n"
            "3. Identify unsupported or questionable claims.\n"
            "4. Identify source-quality problems.\n"
            "5. Suggest a corrected version when necessary.\n\n"
            "Use the web_search tool when additional verification is needed.\n\n"
            "Classify findings as:\n"
            "- VERIFIED\n"
            "- PARTIALLY VERIFIED\n"
            "- UNSUPPORTED\n"
            "- NEEDS MORE EVIDENCE\n\n"
            "Do not invent evidence or sources."
        ),

        expected_output=(
            "A fact-checking report showing the verification status of "
            "each major claim, evidence used, source quality, and corrections "
            "where necessary."
        ),

        agent=fact_checker,

        context=[search_task, analysis_task],
    )

    # ==================================================
    # Task 4 — Final Technical Report
    # ==================================================

    writing_task = Task(
        description=(
            "Write a professional technical research report about {topic}.\n\n"
            "Use the research, analysis, and fact-checking results provided "
            "by the previous agents.\n\n"
            "The report must contain exactly these major sections:\n\n"
            "# Executive Summary\n"
            "# Key Findings\n"
            "# Detailed Analysis\n"
            "# Limitations and Uncertainty\n"
            "# Conclusion\n"
            "# Sources\n\n"
            "Only include claims that are verified or clearly marked as "
            "uncertain by the fact checker.\n\n"
            "Do not invent facts, statistics, citations, or URLs.\n"
            "Keep the writing professional and suitable for a technical "
            "research portfolio project."
        ),

        expected_output=(
            "A clean Markdown technical research report with an executive "
            "summary, key findings, detailed analysis, limitations, "
            "conclusion, and source list."
        ),

        agent=writer,

        context=[
            search_task,
            analysis_task,
            fact_check_task,
        ],
    )

    return search_task, analysis_task, fact_check_task, writing_task

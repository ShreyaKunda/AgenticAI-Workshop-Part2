from crewai import Agent, Task, Crew, LLM
import csv
from pathlib import Path


# Always resolve paths relative to the repository root.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "incident_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "incident_report.md"


llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)


with open(DATA_FILE, newline="", encoding="utf-8") as file:
    incident_data = list(csv.DictReader(file))

data_text = "\n".join(str(row) for row in incident_data)


# ---------------------------------------------------------
# Agents
# ---------------------------------------------------------

incident_manager = Agent(
    role="Incident Manager",
    goal="Understand the incident, establish the investigation scope, and identify the key areas that need to be investigated.",
    backstory="You are an experienced incident manager who establishes a clear incident overview and keeps the investigation focused on evidence.",
    llm=llm,
    verbose=True
)

log_analyst = Agent(
    role="Log and Data Analyst",
    goal="Analyse the incident data and identify anomalies, trends, changes, and important error patterns.",
    backstory="You are a data analyst who specializes in examining system logs and time-series data to identify unusual behaviour and patterns.",
    llm=llm,
    verbose=True
)

technical_investigator = Agent(
    role="Technical Investigator",
    goal="Interpret the available evidence and identify possible technical causes of the incident.",
    backstory="You are a technical investigator who uses system behaviour, error information, and data patterns to develop evidence-based explanations for incidents.",
    llm=llm,
    verbose=True
)

root_cause_analyst = Agent(
    role="Root Cause Analyst",
    goal="Determine the most likely root cause of the incident by comparing investigation findings and supporting evidence.",
    backstory="You are a root cause analyst who evaluates competing explanations and distinguishes evidence-based conclusions from assumptions.",
    llm=llm,
    verbose=True
)

report_generator = Agent(
    role="Technical Report Generator",
    goal="Create a clear and structured technical incident report based only on the investigation findings and available evidence.",
    backstory="You are a technical writer who turns complex investigation findings into concise, well-structured incident reports.",
    llm=llm,
    verbose=True
)


# ---------------------------------------------------------
# Tasks
# ---------------------------------------------------------

incident_task = Task(
    description=f"""
    Review the incident data and create an initial incident overview.

    INCIDENT DATA:
    {data_text}

    Identify the affected system/component, relevant time period, important
    status changes, and the main areas that require investigation.
    Do not assume information that is not supported by the data.
    """,
    expected_output="A concise incident overview containing the affected component, relevant timeline, major status changes, and investigation areas.",
    agent=incident_manager
)

log_analysis_task = Task(
    description=f"""
    Analyse the incident data as a data and log specialist.

    INCIDENT DATA:
    {data_text}

    Identify anomalies, trends, status changes, error codes and timing patterns.
    Highlight changes that occurred before the incident and support findings
    with specific evidence from the data.
    """,
    expected_output="A structured evidence-based analysis of anomalies, trends, status changes, error patterns, and important observations.",
    agent=log_analyst,
    context=[incident_task],
    async_execution=True
)

# This task runs in parallel with log_analysis_task.
# It cannot depend on another asynchronous task, so it uses the incident overview
# and the raw incident data rather than the Log/Data Analyst's output.
technical_task = Task(
    description=f"""
    Use the incident overview and the raw incident data to investigate possible
    technical causes of the incident.

    INCIDENT DATA:
    {data_text}

    Develop multiple plausible explanations where appropriate, connect each
    explanation to the available evidence, and clearly distinguish evidence
    from assumptions. Do not claim that a cause is confirmed unless the data
    supports that conclusion.
    """,
    expected_output="A technical investigation listing plausible causes, reasoning, supporting evidence, alternative explanations, and uncertainty.",
    agent=technical_investigator,
    context=[incident_task],
    async_execution=True
)

root_cause_task = Task(
    description="""
    Review the findings from the Log and Data Analyst and Technical Investigator.
    Compare the proposed causes and determine which explanation is best supported
    by the available evidence. Explain why it is stronger than alternatives and
    identify any uncertainty or missing information.
    """,
    expected_output="A reasoned root-cause assessment identifying the most likely cause, supporting evidence, alternative explanations, confidence, and limitations.",
    agent=root_cause_analyst,
    context=[log_analysis_task, technical_task]
)

report_task = Task(
    description="""
    Create a clear technical incident report using all completed investigation findings.

    Include these sections:
    1. Executive Summary
    2. Incident Overview
    3. Key Findings
    4. Supporting Evidence
    5. Timeline
    6. Possible Causes
    7. Most Likely Root Cause
    8. Impact
    9. Recommended Actions
    10. Confidence and Limitations

    Clearly distinguish observed evidence from assumptions. Do not introduce
    unsupported facts.
    """,
    expected_output="A structured technical incident report with the ten requested sections, evidence-based conclusions, practical recommendations, and confidence/limitations.",
    agent=report_generator,
    context=[incident_task, log_analysis_task, technical_task, root_cause_task]
)


crew = Crew(
    agents=[
        incident_manager,
        log_analyst,
        technical_investigator,
        root_cause_analyst,
        report_generator
    ],
    tasks=[
        incident_task,
        log_analysis_task,
        technical_task,
        root_cause_task,
        report_task
    ],
    verbose=True
)


result = crew.kickoff()

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(str(result))

print("\nInvestigation complete.")
print(f"Report saved to: {OUTPUT_FILE.relative_to(BASE_DIR)}")

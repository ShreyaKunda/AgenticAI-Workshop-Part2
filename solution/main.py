from crewai import Agent, Task, Crew, LLM
import csv
from pathlib import Path

llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "incident_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "incident_report.md"

with open(DATA_FILE, "r", encoding="utf-8") as file:
    data = list(csv.DictReader(file))

incident_manager = Agent(
    role="Incident Manager",
    goal="Establish a clear incident overview and investigation scope from the available data.",
    backstory="You define the incident window, affected system, symptoms, and investigation questions.",
    llm=llm, verbose=True
)

log_analyst = Agent(
    role="Log/Data Analyst",
    goal="Analyze incident data and identify important anomalies, trends, and patterns.",
    backstory="You are a careful data analyst who separates observed facts from interpretations.",
    llm=llm, verbose=True
)

technical_investigator = Agent(
    role="Technical Investigator",
    goal="Interpret the technical evidence and propose plausible causes for the incident.",
    backstory="You investigate technical failures and compare possible explanations against available evidence.",
    llm=llm, verbose=True
)

root_cause_analyst = Agent(
    role="Root Cause Analyst",
    goal="Combine independent findings and determine the most likely root cause while stating uncertainty.",
    backstory="You compare evidence, distinguish symptoms from causes, and avoid unsupported conclusions.",
    llm=llm, verbose=True
)

report_generator = Agent(
    role="Report Generator",
    goal="Create a clear, structured incident report based only on the investigation findings.",
    backstory="You communicate technical investigations clearly and distinguish facts, analysis, hypotheses, and uncertainty.",
    llm=llm, verbose=True
)

incident_task = Task(
    description="Review the incident data and establish the affected system, incident window, observed symptoms, impact, and key questions the investigation should answer. Do not claim a root cause yet.",
    expected_output="A concise incident overview containing the system, timeframe, symptoms, impact, and investigation scope.",
    agent=incident_manager
)

log_analysis_task = Task(
    description="Analyze the provided incident CSV. Identify important changes in status, error codes, temperature, pressure, load, and throughput. Highlight trends leading up to the stoppage and clearly separate observations from interpretations.",
    expected_output="A structured data analysis containing key observations, trends, anomalies, and evidence relevant to the incident.",
    agent=log_analyst,
    context=[incident_task],
    async_execution=True
)

technical_task = Task(
    description="Using the incident scope and available data, investigate plausible technical explanations. Consider overheating, overload, pressure-related issues, sensor problems, cooling problems, and control-system issues. Rank explanations by evidence and clearly state what remains unconfirmed.",
    expected_output="A technical investigation listing plausible causes, supporting evidence, weaknesses, and additional evidence needed for validation.",
    agent=technical_investigator,
    context=[incident_task],
    async_execution=True
)

root_cause_task = Task(
    description="Compare the independent data analysis and technical investigation. Determine the most likely root cause, distinguish root cause from symptoms, identify conflicting evidence, and state an appropriate confidence level. Do not invent missing evidence.",
    expected_output="A reasoned root-cause assessment with supporting evidence, alternative explanations, confidence, and evidence gaps.",
    agent=root_cause_analyst,
    context=[log_analysis_task, technical_task]
)

report_task = Task(
    description="Create a concise incident report using the investigation findings. Include an executive summary, timeline, evidence, analysis, likely root cause, confidence and uncertainty, impact, recommendations, and follow-up actions. Clearly distinguish observed facts from inferred conclusions.",
    expected_output="A structured Markdown incident report suitable for review by an engineering or operations team.",
    agent=report_generator,
    context=[incident_task, log_analysis_task, technical_task, root_cause_task]
)

crew = Crew(
    agents=[incident_manager, log_analyst, technical_investigator, root_cause_analyst, report_generator],
    tasks=[incident_task, log_analysis_task, technical_task, root_cause_task, report_task],
    verbose=True
)

result = crew.kickoff(inputs={"incident_data": data})
OUTPUT_DIR.mkdir(exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(str(result))

print(f"\nIncident report saved to: {OUTPUT_FILE}")

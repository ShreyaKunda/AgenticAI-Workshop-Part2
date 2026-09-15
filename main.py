from crewai import Agent, Task, Crew, LLM
import csv
from pathlib import Path

llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "incident_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "incident_report.md"


def load_incident_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


data = load_incident_data()

incident_manager = Agent(
    role="TODO",
    goal="TODO",
    backstory="TODO",
    llm=llm,
    verbose=True
)

log_analyst = Agent(
    role="TODO",
    goal="TODO",
    backstory="TODO",
    llm=llm,
    verbose=True
)

technical_investigator = Agent(
    role="TODO",
    goal="TODO",
    backstory="TODO",
    llm=llm,
    verbose=True
)

root_cause_analyst = Agent(
    role="TODO",
    goal="TODO",
    backstory="TODO",
    llm=llm,
    verbose=True
)

report_generator = Agent(
    role="TODO",
    goal="TODO",
    backstory="TODO",
    llm=llm,
    verbose=True
)

incident_task = Task(
    description="TODO",
    expected_output="TODO",
    agent=incident_manager
)

log_analysis_task = Task(
    description="TODO",
    expected_output="TODO",
    agent=log_analyst,
    context=[incident_task],
    async_execution=True
)

technical_task = Task(
    description="TODO",
    expected_output="TODO",
    agent=technical_investigator,
    context=[incident_task],
    async_execution=True
)

root_cause_task = Task(
    description="TODO",
    expected_output="TODO",
    agent=root_cause_analyst,
    context=[log_analysis_task, technical_task]
)

report_task = Task(
    description="TODO",
    expected_output="TODO",
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

result = crew.kickoff(inputs={"incident_data": data})

OUTPUT_DIR.mkdir(exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write(str(result))

print(f"\nIncident report saved to: {OUTPUT_FILE}")

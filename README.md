# Agentic AI Workshop — Part 2

Part 2 is a guided capstone activity. You will build a small AI incident investigation team using **CrewAI + Ollama + a local LLM**.

Part 1 introduced individual agents, tasks, tools, specialized agents, and a sequential Crew. Part 2 combines those ideas into a more realistic multi-agent workflow.

## What You Will Build

The system investigates an incident from a CSV dataset and produces a structured incident report.

```text
                 Incident Data
                      |
                      v
               Incident Manager
                      |
           +----------+----------+
           |                     |
           v                     v
    Log/Data Analyst     Technical Investigator
           |                     |
           +----------+----------+
                      |
                      v
               Root Cause Analyst
                      |
                      v
                Report Generator
                      |
                      v
                 Incident Report
```

The Log/Data Analyst and Technical Investigator work independently before their findings are combined by the Root Cause Analyst.

## Learning Goals

By the end of this activity, you should understand:

- how to design specialized agent roles
- how roles, goals, and backstories shape agent behavior
- how Tasks define specific work
- how `context` passes information between tasks
- why some tasks can run independently
- how asynchronous execution can reduce unnecessary waiting
- how multiple perspectives can be combined
- why evidence, uncertainty, and human validation matter in AI systems

## Run the Capstone

Part 2 uses the same Python, CrewAI, and Ollama environment prepared in Part 1.

From the repository root:

```bash
python main.py
```

The completed workflow writes the final report to:

```text
output/incident_report.md
```

## Your Task

Open `main.py` and complete the TODO sections.

Think about what each agent should contribute before writing its instructions. The objective is not just to make the code run, but to design a sensible investigation workflow.

A completed version is available in `solution/main.py` for reference after you attempt the activity.

## Repository Structure

```text
AgenticAI-Workshop-Part2/
├── README.md
├── .gitignore
├── main.py
├── data/
│   └── incident_data.csv
├── output/
│   └── .gitkeep
└── solution/
    └── main.py
```

## Investigation Team

| Agent | Responsibility |
| --- | --- |
| Incident Manager | Establishes the incident overview and investigation scope |
| Log/Data Analyst | Finds anomalies, trends, and patterns in the incident data |
| Technical Investigator | Interprets technical evidence and proposes possible causes |
| Root Cause Analyst | Combines findings and evaluates the most likely cause |
| Report Generator | Turns the investigation into a structured incident report |

## Important Design Idea

The workflow is not simply a chain of five agents.

The two investigation agents can work independently because neither needs the other's output. Their findings are then passed to the Root Cause Analyst.

This gives us:

```text
Agent → [Agent + Agent] → Agent → Agent
```

That is an important step toward designing non-linear agentic workflows.

## Think About It

Before trusting an AI-generated incident investigation, ask:

- Which statements are directly supported by data?
- Which statements are interpretations or hypotheses?
- What evidence is missing?
- What happens if two agents disagree?
- Where should a human review the result?

A multi-agent system does not automatically make an answer correct. Good architecture also requires validation, monitoring, appropriate permissions, and human oversight.

# CrewAI Workshop — Part 2: AI Incident Investigation

In Part 1, you built individual agents and then combined them into a sequential CrewAI workflow.

In Part 2, you will build a small **AI incident investigation team** using CrewAI and a local Ollama model.

The application structure is already provided. Your job is to decide what each specialist should do, how the agents should collaborate, and what evidence they should use.

## What You Will Build

A five-agent investigation workflow:

```text
                    Incident Data
                         |
                         v
                [Incident Manager]
                         |
              +----------+----------+
              |                     |
              v                     v
       [Log/Data Analyst]   [Technical Investigator]
              |                     |
              +----------+----------+
                         |
                         v
                [Root Cause Analyst]
                         |
                         v
                 [Report Generator]
                         |
                         v
                  Incident Report
```

The two investigation agents run independently so that the workflow can collect different perspectives before asking another agent to determine the most likely root cause.

## Learning Goals

By the end of this activity, you should be able to:

- design specialized agent roles for a real-world problem
- write useful agent goals and backstories
- design tasks with clear instructions and expected outputs
- pass information between CrewAI tasks using `context`
- use asynchronous tasks for independent investigation work
- combine multiple findings into a final report
- think about evidence, uncertainty, and human validation

## Run the Application

Make sure your Part 1 CrewAI/Ollama environment is already set up.

After completing the TODOs:

```bash
python main.py
```

The generated report will be written to:

```text
output/incident_report.md
```

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

`main.py` contains intentional TODOs for the workshop. `solution/main.py` contains a completed version for comparison after the activity.

Part 2 assumes the Python, CrewAI, and Ollama setup from Part 1 and does not repeat installation instructions.

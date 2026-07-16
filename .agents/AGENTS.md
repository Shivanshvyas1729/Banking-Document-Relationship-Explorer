# Workspace Rules: Interconnected Document System
first 
give me file name that u code in the manner to guide me if a have to write everthing myself so from where to start every phase

To ensure logical control and system architecture integrity, we follow the **Master Sequence** for project artifacts before writing code:

| Order | Phase | Filename | Purpose |
| --- | --- | --- | --- |
| **1** | **Vision** | `docs/01_scope.md` | The "Why" and "What." Define the ultimate goal. |
| **2** | **Features** | `docs/02_requirements.md` | The "User Stories." What exactly does the user see/do? |
| **3** | **Data** | `docs/03_schema.md` | The "Skeleton." Define all objects and their attributes. |
| **4** | **Logic** | `docs/04_flowchart.md` | The "Brain." Write the step-by-step logic in plain English. |
| **5** | **Structure** | `docs/05_architecture.txt` | The "Map." List all folders and files needed. |
| **6** | **Contract** | `docs/06_api_definitions.json` | The "Handshake." How do pieces communicate? |
| **7** | **Execution** | `docs/07_implementation_plan.md` | The "Order." Which file gets built first? |

## The "Independent Logic" Test
- Always define the logic of a specific feature in `docs/04_flowchart.md` using only plain English before writing code.
- If code is written, review it and update the flowchart to reflect findings. Fix bugs in the flowchart first, then update the code.

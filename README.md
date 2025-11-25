# todo-agent
Helpful AI Agent that listens to your goal, produces a to-do list, and then executes that to-do list.

##  Project Structure

```
todo-agent/
├── agent.py              # Core agent logic & graph definition
├── tools.py              # Tool implementations
├── main.py               # Entry point
├── tests.py              # Tests
├── dependencies.txt      # Python dependencies
├── .env                  # API keys (you have to create this)
└── README.md            # This file
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r dependencies.txt
```

### 2. Set Up API Keys

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-proj-your_openai_key_here
TAVILY_API_KEY=tvly-your_tavily_key_here
```

- **OpenAI API Key**: Required - Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Tavily API Key**: Required for web search - Get from [Tavily](https://tavily.com) (free tier available)

### 3. Run the Agent

To run the agent, run:

```bash
python main.py
```

You'll be prompted to:
1. Choose execution mode. Choose from either "auto" (which runs the to-do list immediately after generation) or "confirm" (which waits for human confirmation before running the to-do list)
2. Enter your goal. The agent works better when the goal is more specific.


##  High-Level Graph Workflow 

The agent follows a **plan-execute-reflect** cycle implemented as a state machine using LangGraph. 

The agent takes as input a high-level goal provided by the user. It first creates a to-do list towards achieving that goal. If the user selected "confirm" mode, then the agent waits for the user's confirmation to begin executing the to-do list. If the user selected "auto" mode, then the agent directly begins executing the to-do list.

The execution loop is as follows. First, the agent selects the next task to execute. It then executes the task using a tool-bound LLM. It then reflects on the status of the task - whether it is completed, failed, or needs follow-up. When all tasks are complete, the agent generates a final summarizing statement and passes it to the user. 

The workflow is visualized here:

![Agent Workflow](images/agent_workflow.png)


## Specific Implementation Details

### State Management
Uses LangGraph's `StateGraph` with `AgentState` TypedDict:

```python
class AgentState(TypedDict):
    goal: str                    # User's original goal
    mode: Literal["confirm", "auto"]
    tasks: list[Task]            # Generated task list
    current_task_id: int | None  # Currently executing task
    approved: bool               # 'True' when the user has approved the to-do list in 'confirm' mode
    conversation_history: list   # Context across tasks
    output: str | None           # Final result
```

###  Available Tools

The agent has access to these tools during execution:

- **`web_search(query)`** - Search the web using Tavily API
- **`read_file(path)`** - Read file contents
- **`write_file(path, content)`** - Write or overwrite files
- **`append_to_file(path, content)`** - Append to existing files

### Specific Step-by-Step Walkthrough of Workflow

#### 1. **Planning Phase** (`generate_todos`)
- User provides a high-level goal
- LLM receives goal and generates structured task list (3-10 tasks)
- Uses Pydantic schema validation to ensure proper task format
- Each task gets: `id`, `title`, `description`, `status` ("pending")
- Tasks stored in agent state for execution

#### 2. **Execution Phase** (Loop)

**Task Selection** (`select_next_task`):
- Iterates through task list
- Finds first task with `status == "pending"`
- Sets as `current_task_id`

**Task Execution** (`execute_task`):
- Retrieves current task details
- Sends to LLM with:
  - Task title & description
  - Conversation history (context from previous tasks)
  - Available tools
- LLM can call one or multiple tools to complete task
- All tool results or LLM outputs accumulated and stored

**Reflection** (`reflect`):
- LLM analyzes task execution result
- Determines status: `"successful"`, `"failed"`, or `"needs follow-up"`
- Updates task status to `"complete"`, `"failed"`, or `"needs-follow-up"`
- Provides brief explanation/summary

**Loop Control** (`has_more_tasks`):
- Checks if any tasks remain with `status == "pending"`
- If yes: loop back to `select_next_task`
- If no: move to completion

#### 3. **Completion Phase** (`reflect_and_complete`)
- LLM generates final summary based on all task results
- Outputs comprehensive answer to original goal



## Execution Modes

### Auto Mode (Default)
- Tasks execute automatically without interruption
- Best for trusted, well-defined goals
- Faster execution

### Confirm Mode
- Shows generated task list before execution
- User can approve or reject
- Useful for reviewing plan before committing


## Testing

The tests.py file includes tests for:
- Pydantic schema validation
- Some of the individual node functions
- Graph compliation

Everything else was tested by running the agent.

In the test file, write the functions you want to test in the '__main__' call and run:
```bash
python tests.py
```




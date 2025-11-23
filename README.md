# todo-agent
Helpful AI Agent that listens to your goal, produces a to-do list, and then executes that to-do list.


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

##  How The Loop Works

### The Execution Loop

The agent follows a **plan-execute-reflect** cycle implemented as a state machine using LangGraph:

```
START
  ↓
generate_todos (Planning Phase)
  ↓
[Mode Check]
  ├─ Auto Mode → select_next_task
  └─ Confirm Mode → display_and_wait_for_approval
                       ↓
                   [User approves?]
                     ├─ Yes → select_next_task
                     └─ No → END
  ↓
EXECUTION LOOP:
  select_next_task
    ↓
  execute_task (with tools)
    ↓
  reflect (assess task status)
    ↓
  [More pending tasks?]
    ├─ Yes → select_next_task (loop)
    └─ No → reflect_and_complete
              ↓
            END
```

### Chat-Planning → Execution Implementation

#### 1. **Planning Phase** (`generate_todos`)
- User provides a high-level goal
- LLM receives goal and generates structured task list (3-10 tasks)
- Uses Pydantic schema validation to ensure proper task format
- Each task gets: `id`, `title`, `description`, `status` ("pending")
- Tasks stored in agent state for execution

```python
class TaskSchema(BaseModel):
    id: int
    title: str
    description: str

# LLM generates: [Task1, Task2, Task3, ...]
```

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
- All tool results accumulated and stored

**Reflection** (`reflect`):
- LLM analyzes task execution result
- Determines status: `"successful"`, `"failed"`, or `"needs follow-up"`
- Updates task status to `"complete"`, `"failed"`, or `"needs-follow-up"`
- Provides brief explanation

**Loop Control** (`has_more_tasks`):
- Checks if any tasks remain with `status == "pending"`
- If yes → loop back to `select_next_task`
- If no → move to completion

#### 3. **Completion Phase** (`reflect_and_complete`)
- LLM generates final summary based on all task results
- Outputs comprehensive answer to original goal

## 🛠️ Available Tools

The agent has access to these tools during execution:

- **`web_search(query)`** - Search the web using Tavily API
- **`read_file(path)`** - Read file contents
- **`write_file(path, content)`** - Write or overwrite files
- **`append_to_file(path, content)`** - Append to existing files
- **`list_files(directory)`** - List directory contents
- **`execute_python(code)`** - Run Python code snippets (sandboxed)
- **Math tools** - `add`, `subtract`, `multiply`, `divide`, `power`

## 🎯 Execution Modes

### Auto Mode (Default)
- Tasks execute automatically without interruption
- Best for trusted, well-defined goals
- Faster execution

### Confirm Mode
- Shows generated task list before execution
- User can approve or reject
- Useful for reviewing plan before committing

## 🏗️ Architecture

### State Management
Uses LangGraph's `StateGraph` with `AgentState` TypedDict:

```python
class AgentState(TypedDict):
    goal: str                    # User's original goal
    mode: Literal["confirm", "auto"]
    tasks: list[Task]            # Generated task list
    current_task_id: int | None  # Currently executing task
    conversation_history: list   # Context across tasks
    output: str | None           # Final result
```

### Graph Nodes
- **generate_todos**: LLM planning with structured output
- **display_and_wait_for_approval**: Human-in-the-loop checkpoint
- **select_next_task**: Task queue management
- **execute_task**: Tool-calling execution
- **reflect**: Post-execution analysis
- **reflect_and_complete**: Final summarization

### Key Features
- ✅ **Stateful execution**: Context maintained across all tasks
- ✅ **Multi-tool support**: Agent can call multiple tools per task
- ✅ **Self-reflection**: Automatic success/failure detection
- ✅ **Error handling**: Graceful handling of tool failures
- ✅ **Configurable limits**: Adjustable recursion limit for complex workflows

## 📁 Project Structure

```
todo-agent/
├── agent.py              # Core agent logic & graph definition
├── tools.py              # Tool implementations
├── main.py               # Entry point
├── tests.py              # Unit tests
├── dependencies.txt      # Python dependencies
├── .env                  # API keys (create this)
└── README.md            # This file
```

## 🔍 Visualizing the Workflow

```python
from agent import print_graph_ascii

print_graph_ascii()  # Prints workflow diagram
```

## 🧪 Testing

Run tests:
```bash
python tests.py
```

Tests include:
- Pydantic schema validation
- Graph compilation
- Individual node functions
- File operation tools
- Math tools
- Web search (if API key present)

## 🔧 Configuration

### Increase Task Limit
Edit `main.py` to increase recursion limit:
```python
config = {
    "recursion_limit": 100  # Default: allows ~25 tasks
}
```

### Change LLM Model
Edit `agent.py`:
```python
llm = ChatOpenAI(model="gpt-4", temperature=0)  # Use GPT-4
```

## 📝 Example Usage

**Goal**: "Research the latest AI news and create a summary report"

**Generated Tasks**:
1. Search for latest AI news
2. Extract key information
3. Write summary to file

**Execution**:
- Task 1: Calls `web_search("latest AI news 2025")`
- Task 2: Calls `execute_python(code to parse results)`
- Task 3: Calls `write_file("ai_summary.txt", summary)`

**Output**: Summary report saved + final overview

## 🤝 Contributing

Feel free to add new tools in `tools.py`:
```python
@tool
def your_tool(arg: str) -> str:
    """Tool description for LLM."""
    # Implementation
    return result

# Add to AVAILABLE_TOOLS list
```

## 📄 License

MIT

from agent import create_agent_graph, AgentState
from dotenv import load_dotenv
import os

def main():
    # Load API key
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in .env file")
        return
    
    # Get user's goal
    print("+ AI Agent TODO Executor +")
    print("=" * 50)
    
    # Ask for mode
    print("\nSelect mode:")
    print("  [1] Auto - Execute tasks automatically")
    print("  [2] Confirm - Review tasks before execution")
    mode_choice = input("\nYour choice (default: 1): ").strip()
    
    mode = "confirm" if mode_choice == "2" else "auto"
    
    goal = input("\nWhat would you like me to help you with? ").strip()
    
    if not goal:
        print("No goal provided. Exiting.")
        return
    
    # Create the graph
    app = create_agent_graph()
    
    # Initialize state
    initial_state = {
        "goal": goal,
        "mode": mode,
        "tasks": None,
        "current_task_id": None,
        "approved": (mode == "auto"),  # Auto mode is pre-approved
        "user_action": None,
        "conversation_history": [],
        "output": None
    }
    
    # Run the agent
    config = {"configurable": {"thread_id": "1"}}
    #print(f"\nGoal: {goal}\n")
    print("Great! Writing up the to-do list...")

    for event in app.stream(initial_state, config):
        pass  # Nodes print their own output
    
    # Get final state
    final_state = app.get_state(config).values
    if final_state.get("output"):
        print("\n" + "=" * 50)
        print("FINAL RESULT")
        print("=" * 50)
        print(final_state["output"])



if __name__ == "__main__":
    main()
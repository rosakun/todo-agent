from agent import *


"""
Tests for small components of the AI agent
"""

def test_pydantic_schemas():
    """ Tests the Pydantic schemas defined in agent.py """
    try:
        task = TaskSchema(id=1, title="Test Task", description="This is a test task.")
        assert task.id == 1, f"Expected id=1, got {task.id}"
        assert task.title == "Test Task", f"Expected title='Test Task', got '{task.title}'"
        assert task.description == "This is a test task.", f"Expected description='This is a test task.', got '{task.description}'"

        todo_list = TodoListSchema(tasks=[task])
        assert len(todo_list.tasks) == 1, f"Expected 1 task, got {len(todo_list.tasks)}"
        assert todo_list.tasks[0].title == "Test Task", f"Expected first task title='Test Task', got '{todo_list.tasks[0].title}'"
        print("test_pydantic_schemas passed.")

    except AssertionError as e:
        print(f"test_pydantic_schemas failed: {e}")
    except Exception as e:
        print(f"test_pydantic_schemas exception: {e}")


""" Test agent nodes """

def test_generate_todos_node(state: AgentState | None = None): # You can test a custom state, otherwise default state is tested
    if state is None:
        state = AgentState({
            "goal": "Plan a birthday party",
            "mode": "auto",
            "tasks": None,
            "current_task_id": None,
            "approved": False,
            "conversation_history": [],
            "output": None
        })
    try:
        new_state = generate_todos(state)
        assert new_state["tasks"] is not None, "Tasks should not be None after generation"
        print(new_state)
        return new_state
    except AssertionError as e:
        print(f"test_generate_todos_node failed: {e}")
    except Exception as e:
        print(f"test_generate_todos_node exception: {e}")


def test_select_next_task_node(state: AgentState | None = None):
    if state is None:
        state = AgentState({
            "goal": "Plan a birthday party",
            "mode": "auto",
            "tasks": [
                {"id": 1, "title": "Book a venue", "description": "Find and book a suitable venue for the party.", "status": "pending", "result": None},
                {"id": 2, "title": "Send invitations", "description": "Create and send invitations to all guests.", "status": "completed", "result": None},
                {"id": 3, "title": "Arrange catering", "description": "Organize food and drinks for the party.", "status": "pending", "result": None}
            ],
            "current_task_id": None,
            "approved": False,
            "user_action": None,  
            "messages": [],  
            "conversation_history": []
        }) 
    try:
        new_state = select_next_task(state) # type: ignore
        assert new_state["current_task_id"] is not None, "Current task ID should not be None after selection"
        print(f"Selected task ID: {new_state['current_task_id']}")
    except AssertionError as e:
        print(f"test_select_next_task_node failed: {e}")
    except Exception as e:
        print(f"test_select_next_task_node exception: {e}")


def test_execute_task_node(state: AgentState | None = None):
    if state is None:
        state = AgentState({
            "goal": "Calculate 2 + 2 * 5",
            "mode": "auto",
            "tasks": [
                {"id": 1, "title": "Multiply 2 and 5", "description": "Multiply 2 and 5 to get an intermediate result.", "status": "pending", "result": None},
                {"id": 2, "title": "Add 2 to the result", "description": "Add 2 to the intermediate result to get the final answer.", "status": "pending", "result": None}
            ],
            "current_task_id": 1,
            "approved": False,
            "user_action": None,  
            "messages": [],  
            "conversation_history": []
        }) 
    try:
        new_state = execute_task(state) 
        print(new_state)
    except AssertionError as e:
        print(f"test_execute_task_node failed: {e}")
    except Exception as e:
        print(f"test_execute_task_node exception: {e}")
        

def test_reflect_and_complete_node(state: AgentState | None = None):
    if state is None:
        state = AgentState({
            "goal": "Calculate 2 + 2 * 5",
            "mode": "auto",
            "tasks": [
                {"id": 1, "title": "Multiply 2 and 5", "description": "Multiply 2 and 5 to get an intermediate result.", "status": "complete", "result": "10"},
                {"id": 2, "title": "Add 2 to the result", "description": "Add 2 to the intermediate result to get the final answer.", "status": "complete", "result": "12"}
            ],
            "current_task_id": None,
            "approved": False,
            "user_action": None,  
            "messages": [],  
            "conversation_history": ['Executing task #1: Multiply 2 and 5', "Tool 'multiply' executed with arguments {'a': 2, 'b': 5}", 'Result: 10', 'Executing task #2: Add 2 to the result', "Tool 'add' executed with arguments {'a': 10, 'b': 2}", 'Result: 12'],
            "output": None
        }) 
    try:
        new_state = reflect_and_complete(state) 
    except AssertionError as e:
        print(f"test_reflect_and_complete_node failed: {e}")
    except Exception as e:
        print(f"test_reflect_and_complete_node exception: {e}")


""" Test graph compilation """

def test_graph_compilation():
    """
    Test whether the agent workflow graph compiles correctly.
    
    Checks:
    - Graph compiles without errors
    - Graph has the expected nodes
    - Graph has the correct entry point
    - Graph structure is valid
    
    Returns:
        True if all checks pass, False otherwise
    """
    try:
        # Attempt to create and compile the graph
        app = create_agent_graph()
        
        # Check that the app was created
        assert app is not None, "Graph compilation returned None"
        print("Graph compiled successfully")
        
        # Get the graph structure
        graph = app.get_graph()
        
        # Check that nodes exist
        nodes = graph.nodes
        expected_nodes = {"generate_todos", "select_next_task", "execute_task", "reflect_and_complete", "__start__", "__end__"}
        node_keys = set(nodes.keys())
        
        assert expected_nodes.issubset(node_keys), f"Missing nodes. Expected {expected_nodes}, got {node_keys}"
        print(f"All expected nodes present: {expected_nodes}")
        
        # Check that edges exist
        edges = graph.edges
        assert len(edges) > 0, "No edges found in graph"
        print(f"Graph has {len(edges)} edges")
        
        # Verify the graph has a valid entry point
        assert "__start__" in node_keys, "Graph missing __start__ node"
        print("Graph has valid entry point")
        
        print("test_graph_compilation PASSED - Graph structure is valid")
        return True
        
    except AssertionError as e:
        print(f"test_graph_compilation FAILED: {e}")
        return False
    except Exception as e:
        print(f"test_graph_compilation EXCEPTION: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    test_graph_compilation()
    
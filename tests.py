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
            "user_action": None,  
            "messages": [],  
            "conversation_history": []
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


""" Test tools """

def test_file_operations():
    """
    Test file operation tools: write_file, read_file, append_to_file, list_files
    """
    from tools import write_file, read_file, append_to_file, list_files
    import os
    
    print("\n" + "=" * 50)
    print("Testing File Operations")
    print("=" * 50)
    
    test_dir = "test_files"
    test_file = os.path.join(test_dir, "test.txt")
    
    try:
        # Test 1: Write file
        print("\n1. Testing write_file...")
        result = write_file.invoke({"file_path": test_file, "content": "Hello, World!"})
        assert "Successfully wrote" in result, f"write_file failed: {result}"
        assert os.path.exists(test_file), "File was not created"
        print(f"   ✓ {result}")
        
        # Test 2: Read file
        print("\n2. Testing read_file...")
        result = read_file.invoke({"file_path": test_file})
        assert "Hello, World!" in result, f"read_file failed: {result}"
        print(f"   ✓ File read successfully")
        
        # Test 3: Append to file
        print("\n3. Testing append_to_file...")
        result = append_to_file.invoke({"file_path": test_file, "content": "\nAppended text"})
        assert "Successfully appended" in result, f"append_to_file failed: {result}"
        print(f"   ✓ {result}")
        
        # Verify append worked
        result = read_file.invoke({"file_path": test_file})
        assert "Hello, World!" in result and "Appended text" in result, "Append did not preserve original content"
        print(f"   ✓ Content verified after append")
        
        # Test 4: List files
        print("\n4. Testing list_files...")
        result = list_files.invoke({"directory": test_dir})
        assert "test.txt" in result, f"list_files failed to find test.txt: {result}"
        print(f"   ✓ File listed successfully")
        
        # Test 5: Read non-existent file (error handling)
        print("\n5. Testing error handling...")
        result = read_file.invoke({"file_path": "nonexistent.txt"})
        assert "Error" in result or "not found" in result, "Error handling failed for missing file"
        print(f"   ✓ Error handled correctly: {result}")
        
        print("\n✅ test_file_operations PASSED - All file operations work correctly")
        return True
        
    except AssertionError as e:
        print(f"\n❌ test_file_operations FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ test_file_operations EXCEPTION: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        try:
            if os.path.exists(test_file):
                os.remove(test_file)
            if os.path.exists(test_dir) and not os.listdir(test_dir):
                os.rmdir(test_dir)
            print("\n🧹 Cleanup completed")
        except:
            pass


def test_web_search():
    """
    Test web search tool (requires TAVILY_API_KEY in .env)
    """
    from tools import web_search
    import os
    
    print("\n" + "=" * 50)
    print("Testing Web Search")
    print("=" * 50)
    
    if not os.getenv("TAVILY_API_KEY"):
        print("⚠️  SKIPPED: TAVILY_API_KEY not found in environment")
        return None
    
    try:
        print("\n1. Testing web_search with simple query...")
        result = web_search.invoke({"query": "Python programming language"})
        
        assert result is not None, "web_search returned None"
        assert "Error" not in result or "API" in result, f"Search failed: {result}"
        assert len(result) > 50, "Search result too short"
        
        print(f"   ✓ Search returned {len(result)} characters")
        print(f"\n   Sample result:\n   {result[:200]}...")
        
        print("\n✅ test_web_search PASSED - Web search works correctly")
        return True
        
    except AssertionError as e:
        print(f"\n❌ test_web_search FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ test_web_search EXCEPTION: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_math_tools():
    """
    Test basic math operation tools
    """
    from tools import add, subtract, multiply, divide, power
    
    print("\n" + "=" * 50)
    print("Testing Math Tools")
    print("=" * 50)
    
    try:
        # Test add
        result = add.invoke({"a": 5, "b": 3})
        assert result == 8, f"add failed: expected 8, got {result}"
        print("   ✓ add(5, 3) = 8")
        
        # Test subtract
        result = subtract.invoke({"a": 10, "b": 4})
        assert result == 6, f"subtract failed: expected 6, got {result}"
        print("   ✓ subtract(10, 4) = 6")
        
        # Test multiply
        result = multiply.invoke({"a": 7, "b": 6})
        assert result == 42, f"multiply failed: expected 42, got {result}"
        print("   ✓ multiply(7, 6) = 42")
        
        # Test divide
        result = divide.invoke({"a": 20, "b": 5})
        assert result == 4, f"divide failed: expected 4, got {result}"
        print("   ✓ divide(20, 5) = 4")
        
        # Test power
        result = power.invoke({"a": 2, "b": 8})
        assert result == 256, f"power failed: expected 256, got {result}"
        print("   ✓ power(2, 8) = 256")
        
        print("\n✅ test_math_tools PASSED - All math operations work correctly")
        return True
        
    except AssertionError as e:
        print(f"\n❌ test_math_tools FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ test_math_tools EXCEPTION: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


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
    print("\n" + "=" * 60)
    print("RUNNING ALL TESTS")
    print("=" * 60)
    
    # Run tool tests
    test_math_tools()
    test_file_operations()
    test_web_search()
    
    # Run graph test
    test_graph_compilation()
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)
    
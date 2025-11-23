from langchain_core.tools import tool
from tavily import TavilyClient
import os
import subprocess
import traceback

@tool
def web_search(query: str) -> str:
    """
    Search the web for current information using Tavily API.
    Optimized for AI agents to get relevant, high-quality search results.
    
    Args:
        query (str): The search query (e.g., "Python programming tutorials", "latest AI news", "what is quantum computing")
    
    Returns:
        str: Formatted search results with title, content summary, and source URL
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY not found in .env file."
    
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query, max_results=3)
        
        # Handle response - it should be a dict
        if not isinstance(response, dict):
            return f"Unexpected response type from Tavily: {type(response)}"
        
        # Get results list
        results_list = response.get('results', [])
        if not results_list:
            return f"No results found for query: '{query}'"
        
        results = []
        for i, result in enumerate(results_list, 1):
            if not isinstance(result, dict):
                continue
                
            title = result.get('title', 'No title')
            content = result.get('content', 'No description')
            url = result.get('url', '')
            
            results.append(
                f"{i}. {title}\n"
                f"   {content}\n"
                f"   Source: {url}"
            )
        
        if not results:
            return f"No valid results found for query: '{query}'"
        
        return "\n\n".join(results)
    
    except Exception as e:
        error_details = traceback.format_exc()
        return f"Search error: {type(e).__name__}: {str(e)}"


@tool
def read_file(file_path: str) -> str:
    """
    Read the contents of a file.
    
    Args:
        file_path (str): The path to the file to read (e.g., "notes.txt", "data/results.json")
    
    Returns:
        str: The contents of the file, or an error message if the file cannot be read
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"File '{file_path}' contents:\n\n{content}"
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found"
    except PermissionError:
        return f"Error: Permission denied to read '{file_path}'"
    except Exception as e:
        return f"Error reading file: {type(e).__name__}: {str(e)}"



@tool
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file. This will overwrite the file if it exists, or create it if it doesn't.
    
    Args:
        file_path (str): The path to the file to write (e.g., "output.txt", "data/report.md")
        content (str): The content to write to the file
    
    Returns:
        str: Success message or error message
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"Successfully wrote {len(content)} characters to '{file_path}'"
    except PermissionError:
        return f"Error: Permission denied to write to '{file_path}'"
    except Exception as e:
        return f"Error writing file: {type(e).__name__}: {str(e)}"


@tool
def append_to_file(file_path: str, content: str) -> str:
    """
    Append content to the end of a file. Creates the file if it doesn't exist.
    
    Args:
        file_path (str): The path to the file to append to (e.g., "log.txt", "notes.md")
        content (str): The content to append to the file
    
    Returns:
        str: Success message or error message
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)
        
        return f"Successfully appended {len(content)} characters to '{file_path}'"
    except PermissionError:
        return f"Error: Permission denied to append to '{file_path}'"
    except Exception as e:
        return f"Error appending to file: {type(e).__name__}: {str(e)}"


# List of all available tools for the agent
AVAILABLE_TOOLS = [web_search, read_file, write_file, append_to_file]

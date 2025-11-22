from langchain_core.tools import tool
from tavily import TavilyClient
import os
import subprocess

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
        response = client.search(query, max_results=5)
        
        results = []
        for i, result in enumerate(response.get('results', []), 1):
            title = result.get('title', 'No title')
            content = result.get('content', 'No description')
            url = result.get('url', '')
            
            results.append(
                f"{i}. {title}\n"
                f"   {content}\n"
                f"   Source: {url}"
            )
        
        if not results:
            return f"No results found for query: '{query}'"
        
        return "\n\n".join(results)
    
    except Exception as e:
        return f"Search error: {type(e).__name__}: {str(e)}" # TODO: Handle search errors


""" Dummy tools """

@tool
def add(a, b):
    """ 
    Adds two integers.
    Args:
        a (int): The first integer.
        b (int): The second integer.
    Returns:
        int: The sum of the two integers.
    """
    return a + b

@tool
def subtract(a, b):
    """ 
    Subtracts the second integer from the first.
    Args:
        a (int): The first integer.
        b (int): The second integer.
    Returns:
        int: The difference of the two integers.
    """
    return a - b

@tool
def multiply(a, b):
    """ 
    Multiplies two integers.
    Args:
        a (int): The first integer.
        b (int): The second integer.
    Returns:
        int: The product of the two integers.
    """
    return a * b

@tool
def divide(a, b):
    """ 
    Divides the first integer by the second.
    Args:
        a (int): The first integer.
        b (int): The second integer.
    Returns:
        int: The quotient of the two integers.
    """
    return a / b

@tool
def power(a, b):
    """
    Raises the first integer to the power of the second.
    Args:
        a (int): The base integer.
        b (int): The exponent integer.
    Returns:
        int: The result of a raised to the power of b.
    """
    return a ** b


# List of all available tools for the agent
AVAILABLE_TOOLS = [web_search,add, subtract, multiply, divide, power]

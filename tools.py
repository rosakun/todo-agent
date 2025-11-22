from langchain_core.tools import tool
import os
import subprocess

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
AVAILABLE_TOOLS = [add, subtract, multiply, divide, power]

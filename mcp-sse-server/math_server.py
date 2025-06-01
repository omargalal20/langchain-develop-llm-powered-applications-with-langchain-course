# math_server.py

import math

from mcp.server.fastmcp import FastMCP

# Initialize the MCP server with a descriptive name
mcp = FastMCP("Basic Math Server")


# Define mathematical tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract the second number from the first."""
    return a - b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide the first number by the second."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


@mcp.tool()
def power(a: int, b: int) -> int:
    """Raise the first number to the power of the second."""
    return a ** b


@mcp.tool()
def sqrt(a: int) -> float:
    """Calculate the square root of a number."""
    if a < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return math.sqrt(a)


@mcp.tool()
def factorial(a: int) -> int:
    """Calculate the factorial of a number."""
    if a < 0:
        raise ValueError("Cannot calculate the factorial of a negative number.")
    return math.factorial(a)


# Run the MCP server using server sent event transport
if __name__ == "__main__":
    mcp.run(transport="sse")

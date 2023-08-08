"""
Basic mathematical operations.

This module provides useful functions for performing math operations.

Functions:
    - add(arg1, arg2): Perform addition of two numbers.
    - sub(arg1, arg2): Perform subtraction of two numbers.
    - multiply(arg1, arg2): Perform multiplication of two numbers.
    - divide(arg1, arg2): Perform division of two numbers.
    - squareroot(arg): Perform square root of the given number.
"""

from math import sqrt


def add(a: float, b: float) -> float:
    """Perform addition of two numbers.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    int or float: The sum of the two input numbers.
    """
    return a+b


def sub(a: float, b: float) -> float:
    """Perform subtraction of two numbers.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    int or float: The subtraction of the two input numbers.
    """
    return a-b


def multiply(a: float, b: float) -> float:
    """Perform multiplication of two numbers.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    int or float: The product of the two input numbers.
    """
    return a*b


def divide(a: float, b: float) -> float:
    """Perform division of two numbers.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    int or float: The division of the two input numbers.
    """
    return a/b


def square_root(a: float) -> float:
    """Perform square root of the given number.

    Parameters:
    a (int or float): The first number.

    Returns:
    int or float: The square root of the input number.
    """
    return sqrt(a)

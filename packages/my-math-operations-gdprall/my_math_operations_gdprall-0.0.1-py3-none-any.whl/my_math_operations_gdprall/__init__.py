# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 07:32:36 2023

@author: gdprall

my_math_functions

A test for python package development. A group of math functions to test 
development.
"""

def square(x):
    '''
    

    Parameters
    ----------
    x : float
        number to be squared

    Returns
    -------
    y : float
        squared number

    '''
    y = x**2
    return y
def sqrt(x):
    '''
    

    Parameters
    ----------
    x : float
        number to be squared

    Returns
    -------
    y : float
        squared number

    '''
    y = x**(1/2)
    return y
def third_degree_poly(x, C1 = 0, C2 = 0, C3 = 0, C4 = 0,  mod1 = 0, mod2 = 0, 
                    mod3 = 0):
    '''
    

    Parameters
    ----------
    x : float
        independent variable
    C1 : float, optional
        The coefficient in front of the 3rd degree variable. The default is 0.
    C2 : float, optional
        The coefficient in front of the 2nd degree variable. The default is 0.
    C3 : float, optional
        The coefficient in front of the 1st degree variable. The default is 0.
    C4 : float, optional
        The coefficient in front of the 0th degree variable. The default is 0.
    mod1 : float, optional
        The modifier to be placed inside the 3rd degree variable. The default 
        is 0.
    mod2 : float, optional
        The modifier to be placed inside the 2nd degree variable. The default 
        is 0.
    mod3 : float, optional
        The modifier to be placed inside the 1st degree variable. The default 
        is 0.

    Returns
    -------
    out : float
        output of the polynomial

    '''
    out = C1 * (x + mod1) ** 3 + C2 * (x + mod2) ** 2 + C3 * (x + mod3) + C4
    return out
def add_multiply(num1, num2, flag = 'A'):
    '''
    

    Parameters
    ----------
    num1 : float
        first number to add or multiply
    num2 : float
        second number to add or multiply
    flag : String, optional
        The flag to trigger multiplication of addition. 'A' for add, 'M' for
        Multiply The default is 'A'.

    Raises
    ------
    TypeError
        Flag not recognized

    Returns
    -------
    y : float
        output

    '''
    if flag == 'A':
        y = num1 + num2
        return y
    elif flag == 'M':
        y = num1 * num2
        return y
    else:
        raise TypeError('Flag not recognized')
        
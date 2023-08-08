# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:11:34 2023

@author: gdprall
"""
import my_math_operations_gdprall
def test_square():
    assert my_math_operations_gdprall.square(5) == 25
def test_sqrt():
    assert my_math_operations_gdprall.sqrt(81) == 9
def test_third_degree_poly():
    assert my_math_operations_gdprall.third_degree_poly(3, 1) == 27
def test_add_multipl():
    assert my_math_operations_gdprall.add_multiply(2, 3) == 5
    
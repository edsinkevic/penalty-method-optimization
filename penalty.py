import numpy as np
import numpy.linalg as linalg
from calculations import b, g, f, h
from minimize import minimize
from nelder_mead import nelder_mead

points = [[0., 0., 0.], [1., 1., 1.], [0, 3 / 10, 7 / 10]]

def solve_0():
    for point in points:
        print(calculate_point(point))

def solve_1():
    for point in points:
        try_reducing(point, 2, [0.10, 0.20, 0.50, 0.70, 0.99])

def solve_2():
    for point in points:
        try_starting(point, 0.50, [2, 0.2, 0.02, 0.002])

def calculate_point(point):
    f_result = f(point)
    g_result = g(point)
    h_result = h(point)

    return f"f({point}) = {f_result}\ng({point}) = {g_result}\nh({point}) = {h_result}\n"

def try_reducing(point, r, reductions):
    result = "arg min f,r,rc,n_f,n_min,min f\n"
    for reduction in reductions:
        [point, value, f_count, min_count] = solve_one(point, r, reduction)
        result = f"{result}{point},{r},{reduction},{f_count},{min_count},{value}\n"

    print(result)
    return result

def try_starting(point, reduction, rs):
    result = "arg min f,r,rc,n_f,n_min,min f\n"
    for r in rs:
        [point, value, f_count, min_count] = solve_one(point, r, reduction)
        result = f"{result}{point},{r},{reduction},{f_count},{min_count},{value}\n"

    print(result)
    return result

def solve_one(point, r, reduction):
    [result, f_count, min_count] = minimize(point, r, reduction, [])
    return [point, result, f_count, min_count]

solve_0()
solve_1()
solve_2()

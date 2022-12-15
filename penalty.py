import numpy as np
import numpy.linalg as linalg
from calculations import b, g, f, h
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
    global f_count
    global min_count
    f_count = 0
    min_count = 0
    result = minimize(point, r, reduction, [])
    return [point, result, f_count, min_count]

min_count = 0

def minimize(point, r, reduction, last_result, epsilon = 1e-6):
    global min_count
    br = inject_r(r)
    min_count += 1
    result = nelder_mead(br, np.array(point), epsilon = epsilon)

    if not_converging(f, last_result, result):
        return minimize(result, r - r * reduction, reduction, result)
    return result


f_count = 0

def inject_r(r):
    def func(X):
        global f_count
        f_count += 1
        return b(X, r)

    return func

def not_converging(f, last_result, result, epsilon = 1e-6):
    if len(last_result) == 0:
        return True
    if abs(f(last_result) - f(result)) > epsilon:
        return True
    return False

solve_0()
solve_1()
solve_2()

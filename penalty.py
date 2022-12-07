import numpy as np
import numpy.linalg as linalg
from calculations import b, g, f
from nelder_mead import nelder_mead

points = [[0., 0., 0.], [1., 1., 1.], [0, 3 / 10, 7 / 10]]

f_count = 0

def inject_r(r):
    def func(X):
        global f_count
        f_count += 1
        return b(X, r)

    return func

min_count = 0

def minimize(point, r, r_reduction_coef, last_result):
    global min_count
    br = inject_r(r)
    min_count += 1
    result = nelder_mead(br, np.array(point))

    if abs(f(last_result) - f(result)) > 0.000001:
        return minimize(result, r * r_reduction_coef, r_reduction_coef, result)
    return result

def solve(points, r, r_reduction_coef):
    global f_count
    global min_count
    for point in points:
        f_count = 0
        min_count = 0
        result = minimize(point, r, r_reduction_coef, [10, 10, 10])
        print(f'Minimum point starting from {point}:')
        print(f'   Result: {result}')
        print(f'   Penalty function calculation count: {f_count}')
        print(f'   Iterations: {min_count}')

solve(points, 2, 0.50)

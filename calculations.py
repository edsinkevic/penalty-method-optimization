
def f(X):
    x = X[0]
    y = X[1]
    z = X[2]
    return - x * y * z

def g(X):
    x = X[0]
    y = X[1]
    z = X[2]
    return 2 * (x*y + x*z + y*z) - 1

def gp(X):
    return g(X) ** 2

def h(X):
    x = X[0]
    y = X[1]
    z = X[2]
    return -x <= 0 and -y <= 0 and -z <= 0

def hp(X):
    x = X[0]
    y = X[1]
    z = X[2]
    return (max(0, -x) + max(0, -y) + max(0, -z)) ** 2

def b(X, r):
    return f(X) + 1/r * (gp(X) + hp(X))

def calculate_point(point):
    f_result = f(point)
    g_result = g(point)
    h_result = h(point)

    return f"f({point}) = {f_result}\ng({point}) = {g_result}\nh({point}) = {h_result}\n"

def calculate_points(points):
    for point in points:
        print(calculate_point(point))

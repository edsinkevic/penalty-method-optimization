import math

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
    return math.pow(g(X), 2)

def h(X):
    x = X[0]
    y = X[1]
    z = X[2]
    return max(0, -x) + max(0, -y) + max(0, -z)

def hp(X):
    return math.pow(h(X), 2)

def b(X, r):
    return f(X) + 1./float(r) * (gp(X) + hp(X))


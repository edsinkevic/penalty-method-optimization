import copy
import numpy as np
import math


def nelder_mead(f, x_start,
                step=0.1, epsilon=10e-8,
                no_improvement_count_max=30, max_iter=100000,
                alpha=1., gamma=2., rho=0.5, sigma=0.5):
    simplex = init(f, x_start, step)
    previous_best = f(x_start)
    no_improvement_count = 0

    iters = 0
    while 1:
        sort(simplex)

        best = best_score(simplex)

        if max_iter and iters >= max_iter:
            return best_point(simplex)

        iters += 1

        if epsilon < previous_best - best:
            no_improvement_count = 0
            previous_best = best
        else:
            no_improvement_count += 1

        if no_improvement_count >= no_improvement_count_max:
            return best_point(simplex)

        centroid = np.array(calculate_centroid(simplex))

        reflected_x = centroid + alpha * (centroid - worst_point(simplex))
        reflection_score = f(reflected_x)

        if reflection(simplex, f, centroid, reflected_x, reflection_score):
            continue

        if expansion(simplex, f, centroid, reflected_x, reflection_score, gamma):
            continue

        if contraction(simplex, f, centroid, reflected_x, reflection_score, rho):
            continue
        simplex = reduction(simplex, f, sigma)


def init(f, x_start, alpha):
    dim = len(x_start)
    previous_best = f(x_start)
    simplex = [[x_start, previous_best]]

    delta1 = (np.sqrt(dim + 1) + dim - 1) * alpha / (dim * np.sqrt(2))
    delta2 = (np.sqrt(dim + 1) - 1) * alpha / (dim * np.sqrt(2))

    for i in range(dim):
        x = copy.copy(x_start)
        for j in range(dim):
            if j == i:
                x[j] = x_start[j] + delta1
            else:
                x[j] = x_start[j] + delta2
        score = f(x)
        simplex.append([x, score])

    return simplex


def sort(simplex):
    simplex.sort(key=lambda x: x[1])


def calculate_centroid(simplex):
    dim = len(best_point(simplex))
    centroid = [0.] * dim
    for current_x, _ in simplex[:-1]:
        for i, c in enumerate(current_x):
            centroid[i] += c / (len(simplex) - 1)
    return centroid


def reflection(simplex, f, centroid, reflected_x, reflection_score):
    if best_score(simplex) <= reflection_score < second_worst_score(simplex):
        replace_worst(simplex, [reflected_x, reflection_score])
        return True
    return False


def expansion(simplex, f, centroid, reflected_x, reflection_score, gamma):
    if reflection_score < best_score(simplex):
        expansion_x = centroid + gamma * (reflected_x - centroid)
        expansion_score = f(expansion_x)
        if expansion_score < reflection_score:
            replace_worst(simplex, [expansion_x, expansion_score])
            return True

        replace_worst(simplex, [reflected_x, reflection_score])
        return True
    return False


def contraction(simplex, f, centroid, reflected_x, reflection_score, rho):
    if reflection_score < worst_score(simplex):
        contraction_x = centroid + rho * (reflected_x - centroid)
        contraction_score = f(contraction_x)
        if contraction_score < reflection_score:
            replace_worst(simplex, [contraction_x, contraction_score])
            return True
        return False

    contraction_x = centroid + rho * (worst_point(simplex) - centroid)
    contraction_score = f(contraction_x)
    if contraction_score < worst_score(simplex):
        replace_worst(simplex, [contraction_x, contraction_score])
        return True

    return False


def reduction(simplex, f, sigma):
    new_simplex = []
    for current_x, _ in simplex:
        reduction_x = best_point(simplex) + sigma * (current_x - best_point(simplex))
        reduction_score = f(reduction_x)
        new_simplex.append([reduction_x, reduction_score])
    return new_simplex


def replace_worst(simplex, x):
    simplex[-1] = x
    return simplex


def worst_score(simplex):
    return simplex[-1][1]


def best_score(simplex):
    return simplex[0][1]


def worst_point(simplex):
    return simplex[-1][0]


def best_point(simplex):
    return simplex[0][0]


def second_worst_score(simplex):
    return simplex[-2][1]


def without_scores(simplex):
    return list(map(lambda x: x[0], simplex))

import random

import math
import matplotlib.pyplot as plt


def distance(x1, x2, y1, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


def cluster_decision(x, y, c_x, c_y):
    min_distance = distance(x, c_x[0], y, c_y[0])
    cluster = 0
    for _ in range(1, len(c_x)):
        if distance(x, c_x[_], y, c_y[_]) < min_distance:
            cluster = _

    return cluster


def new_centroid(points, n):
    c_x = [None] * n
    c_y = [None] * n

    for _ in range(n):
        c_x[_] = [i[0] for i in points if i[2] == _]
        c_y[_] = [i[1] for i in points if i[2] == _]
        c_x[_] = sum(c_x[_]) / len(c_x[_]) if len(c_x[_]) is not 0 else 0
        c_y[_] = sum(c_y[_]) / len(c_y[_]) if len(c_y[_]) is not 0 else 0

    return c_x, c_y


def main():
    input_points = [[0.1, 0.6, -1], [0.15, 0.71, -1], [0.08, 0.9, -1], [0.16, 0.85, -1], [0.2, 0.3, -1],
                    [0.25, 0.5, -1], [0.24, 0.1, -1], [0.3, 0.2, -1]]

    x = [i[0] for i in input_points]
    y = [i[1] for i in input_points]

    max_x = max(x)
    max_y = max(y)

    k = 2
    # First Centroid
    c_x = [random.uniform(0, max_x) for _ in range(k)]
    c_y = [random.uniform(0, max_y) for _ in range(k)]

    previous_cx = c_x
    previous_cy = c_y

    while c_x == previous_cx and c_y == previous_cy:
        for points in input_points:
            points[2] = cluster_decision(points[0], points[1], c_x, c_y)

        previous_cx = c_x
        previous_cy = c_y

        c_x, c_y = new_centroid(input_points, len(c_x))

    plt.scatter(x, y)
    plt.scatter(c_x, c_y)
    for points in input_points:
        plt.plot([points[0], c_x[points[2]]], [points[1],c_y[points[2]]])
    plt.show()

    print(c_x)
    print(c_y)


main()

import operator

import math

import matplotlib.pyplot as plt


def euclidean_distance(a, b):
    return math.sqrt(math.pow((a[0] - b[0]), 2) + math.pow(a[1] - b[1], 2))


def main():
    data = [[2, 4, 'a'], [4, 2, 'a'], [4, 4, 'b'], [4, 6, 'a'], [6, 2, 'b'], [6, 4, 'a']]
    predict_data = [[6, 6]]

    for _ in range(len(data)):
        distance = euclidean_distance(data[_], predict_data[0])
        data[_].extend([distance])

    sorted_data = sorted(data, key=operator.itemgetter(3))

    k = 2

    nearest_neighbours = sorted_data[:k]

    class_count = {}
    for _ in nearest_neighbours:
        if _[2] not in class_count:
            class_count[_[2]] = 0
        class_count[_[2]] += 1

    sorted_class = sorted(class_count.items(), key=lambda x: x[1], reverse=True)

    print('The point belong to class ' + sorted_class[0][0])

    x = [i[0] for i in data]
    y = [i[1] for i in data]
    plt.scatter(x, y)

    plt.scatter(6, 6)

    nearest_x = [i[0] for i in nearest_neighbours]
    nearest_y = [i[1] for i in nearest_neighbours]

    for _ in range(len(nearest_neighbours)):
        plt.plot([6, nearest_x[_]], [6, nearest_y[_]])

    plt.show()


main()

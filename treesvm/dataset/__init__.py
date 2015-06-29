# dataset
import numpy as np
import csv


class Dataset:
    features = None
    labels = None

    def __init__(self, features, labels):
        self.features = features
        self.labels = labels

    # load dataset from file
    @staticmethod
    def load(file):
        features = []
        labels = []

        with open(file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                features.append(row[:-1])
                labels.append(row[-1])

        data = Dataset(np.array(features).astype(float), np.array(labels))
        return data

    # split a dataset into groups according to its class
    @staticmethod
    def split(dataset):
        classes = {}

        for idx, row in enumerate(dataset.features):
            label = dataset.labels[idx]
            if not label in classes:
                classes[label] = []

            classes[label].append(row)

        # convert normal list into numpy array
        for key, val in classes.items():
            classes[key] = np.array(val)

        return classes

    # find the squared radius of a given class
    @staticmethod
    def squared_radius(all_points, kernel):
        def in_sqrt(a_point):
            # first term of the equation goes here
            a = kernel(a_point, a_point)

            # second term of the equation
            def middle_term(point):
                summation = 0
                for p in all_points:
                    summation += kernel(point, p)
                return -2. / all_points.size * summation

            b = middle_term(a_point)

            # last term of the equation
            # this function doesn't accept any parameters
            def last_term():
                # summation = 0
                # for xx in points:
                #     for yy in points:
                #         summation += kernel(xx, yy)
                # this is the optimized version of the code above
                summation = 0
                for i, xx in enumerate(all_points):
                    summation += kernel(xx, xx)
                    for yy in all_points[i + 1:]:
                        summation += 2 * kernel(xx, yy)
                return 1. / all_points.size ** 2 * summation

            c = last_term()

            # put it all together
            return a + b + c

        # calculate the radius (max of the sqrt thing)
        squared_radius = [in_sqrt(point) for point in all_points]
        for each in squared_radius:
            assert each >= 0
        # return the maximum
        return max(squared_radius)

    # squared distance
    @staticmethod
    def squared_distance(class_a, class_b, kernel):
        # square distance calculations (without sqrt)
        # first term
        def first_term():
            summation = 0
            # normally is the faster form of full nested for loops
            for i, xx in enumerate(class_a):
                summation += kernel(xx, xx)
                for yy in class_a[i + 1:]:
                    summation += 2 * kernel(xx, yy)
            return 1. / class_a.shape[0] ** 2 * summation

        # second term
        def second_term():
            summation = 0
            # this loop cannot be optimized by the factor of two
            for xx in class_a:
                for yy in class_b:
                    summation += kernel(xx, yy)
            return -2. / (class_a.shape[0] * class_b.shape[0]) * summation

        # third term
        def third_term():
            summation = 0
            for i, xx in enumerate(class_b):
                summation += kernel(xx, xx)
                for yy in class_b[i + 1:]:
                    summation += 2 * kernel(xx, yy)
            return 1. / class_b.shape[0] ** 2 * summation

        squared_distance = first_term() + second_term() + third_term()
        assert squared_distance > 0
        return squared_distance

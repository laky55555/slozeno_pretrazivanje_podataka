import math
from abc import ABCMeta, abstractmethod
from numpy import array, newaxis, zeros
from numpy.random import randint


class FindClusters(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def membership(cls, cluster, data_point, clusters, data_points):
        ...

    @classmethod
    @abstractmethod
    def weight(cls, data_point):
        ...

    @classmethod
    @abstractmethod
    def objective(cls, data_points, clusters):
        ...

    @staticmethod
    def initialize_centroides_random(data_points, number_of_clusters):
        centroids = [zeros(len(data_points[0]))] * number_of_clusters
        points_per_centroid = [0] * number_of_clusters
        for point in data_points:
            index = randint(0, number_of_clusters)
            centroids[index] += point
            points_per_centroid[index] += 1
        # TODO: mozda bi trebalo napraviti provjeru da li je
        # points_per_centroid uvijek > 0
        return array(centroids) / array(points_per_centroid)[:, newaxis]
        # return array([c/p for c, p in zip(centroids, points_per_centroid)])

    @staticmethod
    def initialize_centroides_forgy(data_points, number_of_clusters):
        return data_points[randint(len(data_points), size=number_of_clusters)]

    @classmethod
    def recompute_centroids(cls, data_points, centroids):
        # to su koraci 2 i 3
        weights_array = array([cls.weight(data_point)
                               for data_point in data_points])
        #print(weights_array, len(weights_array))
        for i in range(len(centroids)):
            membership_array = array(
                [cls.membership(centroids[i], point, centroids, data_points) for point in data_points])
            #print(membership_array, len(membership_array))
            coefficients_per_point = membership_array * weights_array
            suma = sum(coefficients_per_point)
            if(suma == 0):
                centroids[i] = 0
            else:
                centroids[i] = sum(
                    data_points * coefficients_per_point[:, newaxis]) / sum(coefficients_per_point)

        return centroids

    @classmethod
    def test_algorithm_yield(cls, number_of_iterations, initial_centroides, data_points):
        centroids = initial_centroides
        print("initial_centroides")
        yield centroids
        for i in range(number_of_iterations):
            print("Started", i, "iteration")
            centroids = cls.recompute_centroids(data_points, centroids)
            yield centroids
        return centroids

    @classmethod
    def test_algorithm(cls, number_of_iterations, initial_centroides, data_points):
        centroids = initial_centroides
        for i in range(number_of_iterations):
            print("Started", i, "iteration")
            centroids = cls.recompute_centroids(data_points, centroids)
        return centroids

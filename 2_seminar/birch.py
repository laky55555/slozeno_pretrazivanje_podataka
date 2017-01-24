from math import sqrt
from numpy.random import multivariate_normal
from numpy import array, sum, mean, identity


class BIRCH():
    """Class for constructing dataset for testing clustering algorithms ."""

    def __init__(self, dimensions=(10, 10), number_of_points_per_cluster=100,
                 distance_between_clusters=4 * sqrt(2), cluster_radius=sqrt(2)):
        self.__dict__.update(locals())
        # TODO: napraviti za dimenzije vece od 2

        self.create_centroides()
        self.create_data_points()

    def create_centroides(self):
        self.centroids = []
        height = sqrt(self.distance_between_clusters**2 -
                      (self.distance_between_clusters / 2)**2)
        for i in range(self.dimensions[1]):
            stride = 0 if(i % 2 == 0) else self.distance_between_clusters / 2
            for j in range(self.dimensions[0]):
                self.centroids.append(
                    array([j * self.distance_between_clusters + stride, i * height]))

        # Translating all centroid around (0,0)
        self.centroids -= mean(self.centroids, axis=0)

    def create_data_points(self):
        self.data_points = []
        for i in self.centroids:
            self.data_points.extend(self.create_point(i))

    def create_point(self, centroid):
        mean = centroid
        cov = identity(len(self.dimensions)) # [[1, 0], [0, 1]]
        return multivariate_normal(mean, cov, self.number_of_points_per_cluster)

    def test_data(self, print_radius=False):
        sums_per_cluster = []
        # Radius per claster = sqrt[(sum(Xi - X0)^2)/N] i=1,...N
        # where N is number_of_points_per_cluster and Xi data in claster and X0
        # centroid
        for i in range(len(self.centroids)):
            suma = 0
            for j in range(self.number_of_points_per_cluster):
                suma += sum((self.centroids[i] -
                             self.data_points[i * self.number_of_points_per_cluster + j])**2)
            sums_per_cluster.append(sqrt(
                                    suma / self.number_of_points_per_cluster))

        if(print_radius):
            print("Radius per centroids = ", sums_per_cluster)
        print("Average cluster radius = ", sum(
            sums_per_cluster) / len(sums_per_cluster))

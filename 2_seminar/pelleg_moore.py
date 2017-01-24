from numpy.random import multivariate_normal, rand, randint
from numpy import array, identity


class PellegMoore():
    coefficient = 0.012

    """Class for constructing dataset for testing clustering algorithms ."""

    def __init__(self, dimension=2, number_of_points=2500, number_of_clusters=50, deviation_coefficient=0.012):
        self.__dict__.update(locals())

        self.create_centroides()
        self.create_data_points()

    def create_centroides(self):
        self.centroids = array(
            [rand(self.dimension,) - 0.5 for i in range(self.number_of_clusters)])

    def create_data_points(self):
        self.data_points = [self.create_point(self.centroids[randint(
            0, self.number_of_clusters)]) for i in range(self.number_of_points)]

    def create_point(self, centroid):
        mean = centroid
        cov = (identity(self.dimension) * self.dimension *
               PellegMoore.coefficient)  # [[1, 0], [0, 1]]
        return multivariate_normal(mean, cov, 1)

from numpy.random import rand, randint
from numpy import array, identity

from algorithms import KMeans
from .data_set import DataSet


class PellegMoore(DataSet):
    """Class for constructing dataset for testing clustering algorithms ."""
    # coefficient = 0.00012
    coefficient = 0.012

    def __init__(self, dimension=2, number_of_points=2500, number_of_clusters=50, deviation_coefficient=0.012):
        self.__dict__.update(locals())

        self.create_centroides()
        self.create_data_points()

    def create_centroides(self):
        self.centroids = array(
            [rand(self.dimension,) - 0.5 for i in range(self.number_of_clusters)])

    def create_data_points(self):
        cov = (identity(self.dimension) * self.dimension *
               PellegMoore.coefficient)  # [[1, 0], [0, 1]] * 2 * 0.012
        self.data_points = array([self.create_point(self.centroids[randint(
            0, self.number_of_clusters)], cov, 1)[0] for i in range(self.number_of_points)])

    def check_calculated_centroids(self, calculated_centroids):
        score = KMeans.objective(self.data_points, calculated_centroids)/KMeans.objective(self.data_points, self.centroids)

        self.log_data = {
            'centroids': {
                'true': KMeans.objective(self.data_points, self.centroids),
                'calculated': KMeans.objective(
                    self.data_points,
                    calculated_centroids
                )
            },
            'score': score
        }

        return score

    def print_log_data(self):
        print("""
        True centroids = %f
        Calculated centroids = %f
        Clustering score = %f
        """ % (
            self.log_data['centroids']['true'],
            self.log_data['centroids']['calculated'],
            self.log_data['score']
        ))

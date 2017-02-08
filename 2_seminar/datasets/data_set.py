from numpy.random import multivariate_normal
from abc import ABCMeta, abstractmethod


class DataSet(metaclass=ABCMeta):
    @abstractmethod
    def create_centroides(self):
        ...

    @abstractmethod
    def create_data_points(self):
        ...

    @abstractmethod
    def check_calculated_centroids(self, calculated_centroids):
        ...

    def create_point(self, mean, covariance, number_of_points):
        return multivariate_normal(mean, covariance, number_of_points)

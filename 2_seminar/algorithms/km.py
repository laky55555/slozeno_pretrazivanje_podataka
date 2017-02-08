import math
from algorithms.find_clusters import FindClusters
from numpy.linalg import norm


class KMeans(FindClusters):
    @classmethod
    def objective(cls, data_points, clusters):
        sum = 0
        for x in data_points:
            min = math.inf
            for c in clusters:
                distance = norm(x - c)
                if distance < min:
                    min = distance
            sum += min
        return sum

    @classmethod
    def membership(cls, cluster, data_point, clusters, data_points):
        min = norm(cluster - data_point)
        for c in clusters:
            if norm(c - data_point) < min:
                return 0
        return 1

    @classmethod
    def weight(cls, data_point):
        return 1

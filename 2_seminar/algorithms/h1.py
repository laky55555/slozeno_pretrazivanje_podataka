from numpy.linalg import norm

from .find_clusters import FindClusters


class Hybrid1(FindClusters):
    p = 3.5

    @staticmethod
    def helper(data_point, clusters, number = 0):
        brojnik = 0
        for c in clusters:
            tmp = norm(data_point - c)
            if tmp != 0:
                brojnik += tmp ** (-Hybrid1.p - number)
        return brojnik

    @classmethod
    def objective(cls, data_points, clusters):
        return 0

    @classmethod
    def membership(cls, cluster, data_point, clusters, data_points):
        min = norm(cluster - data_point)
        for c in clusters:
            if norm(c - data_point) < min:
                return 0
        return 1

    @classmethod
    def weight(cls, data_point, clusters):
        brojnik = Hybrid1.helper(data_point, clusters, number=2)
        nazivnik = Hybrid1.helper(data_point, clusters, number=0)

        return brojnik / (nazivnik ** 2)

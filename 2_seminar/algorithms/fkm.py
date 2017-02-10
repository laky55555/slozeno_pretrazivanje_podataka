from numpy.linalg import norm

from .find_clusters import FindClusters


class FuzzyKMeans(FindClusters):
    fuzziness = 2

    @staticmethod
    def helper(data_point, clusters, number = 0):
        brojnik = 0
        for c in clusters:
            tmp = norm(data_point - c)
            if tmp != 0:
                brojnik += tmp ** (-2 / (FuzzyKMeans.fuzziness - 1))
        return brojnik

    @classmethod
    def objective(cls, data_points, clusters):
        return 0

    @classmethod
    def membership(cls, cluster, data_point, clusters, data_points):
        brojnik = norm(data_point - cluster)
        if brojnik != 0:
            brojnik **= (-2 / (FuzzyKMeans.fuzziness - 1))

        nazivnik = FuzzyKMeans.helper(data_point, clusters, number=0)
        return brojnik / nazivnik

    @classmethod
    def weight(cls, data_point, clusters):
        return 1

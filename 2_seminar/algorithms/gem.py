from scipy.stats import multivariate_normal

from .find_clusters import FindClusters


class GaussianExpectationMaximization(FindClusters):
    covariance = 0.012

    # p - Gauss
    @classmethod
    def _p(cls, cluster=None, data_point=None, clusters=None, data_points=None):
        if cluster is None:
            return 1 / len(data_points)

        if data_point is None:
            return 1 / len(clusters)

        return multivariate_normal.pdf(
            data_point,
            mean=cluster,
            cov=cls.covariance
        )

    @classmethod
    def objective(cls, data_points, clusters):
        p = lambda cluster, data_point: cls._p(
            cluster,
            data_point,
            clusters,
            data_points
        )
        f = lambda x, c: p(data_point=x, cluster=c) * p(cluster=c)
        cluster_sums = [
            sum(map(lambda c: f(x, c), clusters)) for x in data_points
        ]

        return sum(map(-math.log, cluster_sums))

    @classmethod
    def membership(cls, cluster, data_point, clusters, data_points):
        return (
            (
                cls._p(data_point=data_point, cluster=cluster) *
                cls._p(cluster=cluster, clusters=clusters)
            ) / cls._p(data_point=data_point, data_points=data_points)
        )

    @classmethod
    def weight(cls, data_point, clusters):
        return 1

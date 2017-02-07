import math
from abc import ABCMeta, abstractmethod
from numpy.linalg import norm
from random import sample
from numpy import array, newaxis, zeros
from numpy.random import randint


class FindClusters(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def membership(cls, cluster, data_point, clusters):
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
                [cls.membership(centroids[i], point, centroids) for point in data_points])
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


#
#
# ##euklidska udaljenost
# ##jednostavnije numpy.linalg.norm()
# def udaljenost(a, b):
#     sum = 0
#     for ai, bi in zip(a, b):
#         sum += (ai - bi) ** 2
#     return math.sqrt(sum)
#
#
# def iteracija(data_points, clusters, m, w):
#     brojnik = data_points[0]
#     for b in brojnik: b = 0
#     nazivnik = 0
#     noviC = set()
#     for cj in clusters:
#         for xi in data_points:
#             nazivnik += m(cj, xi)*w(xi)
#             for xij in xi:
#                 xij *= m(cj, xi)*w(xi)
#             i = 0
#             for bi in brojnik:
#                 bi += xi[i]
#                 ++i
#         for b in brojnik:
#             b /= float(nazivnik)
#         noviC.add(brojnik)
#     return noviC


class KMeans(FindClusters):

    @classmethod
    def objective(cls, data_points, clusters):
        sum = 0
        for x in data_points:
            min = math.inf
            for c in clusters:
                #distance = udaljenost(x, c)**2
                distance = norm(x - c)
                if distance < min:
                    min = distance
            sum += min
        return sum

    @classmethod
    def membership(cls, cluster, data_point, clusters):
        #min = udaljenost(cj, xi)**2
        min = norm(cluster - data_point)
        for c in clusters:
            # if udaljenost(c, xi)**2 < min:
            if norm(c - data_point) < min:
                return 0
        return 1

    @classmethod
    def weight(cls, data_point):
        return 1


# class GaussianExpectationMaximization():
#     ## p - Gauss
#     #TODO: to mi se cini da je 1/broj centroida
#     def p(c):
#         return norm(c, 1).pdf(x)
#
#     #TODO: vjerojatnost da je tocka x generirana gausovom distribucijom
#     def p2(x,c):
#         # TODO: to jos treba napisati
#         return None
#
#
#     def objective(data_points, clusters):
#         rez = 0
#         for x in data_points:
#             b = 0
#             for c in clusters:
#                 b += p2(x, c)*p(c)
#             rez += math.log(b)
#         return -rez
#
#
#     def membership(cj, xi):
#         return p2(xi, cj)*p(cj)/p(xi)
#
#
#     def weight(xi):
#         return 1
#
#
# ##FKM
#
# class FuzzyKMeans():
#     fuzziness = 1
#
#     def objective(U, data_points, clusters):
#         rez = 0
#         for xi in data_points:
#             b = 0
#             for cj in clusters:
#                 # TODO: tu je U membership?!?!?!?
#                 b += U[i][j]**fuzziness * udaljenost(xi, cj)**2
#             rez += b
#         return rez
#
#
#     def membership(r, clusters, cj, xi):
#         brojnik = udaljenost(xi, cj)**(-2/(r-1))
#         nazivnik = 0
#         for c in clusters:
#             nazivnik += udaljenost(xi, c)**(-2/(r-1))
#         return brojnik/nazivnik
#
#
#     def weight(xi):
#         return 1
#
# ##KHM
#
# class KHarmonicMeans:
#     def objective(p, data_points, clusters):
#         rez = 0
#         for xi in data_points:
#             brojnik = len(clusters)
#             nazivnik = 0
#             for cj in clusters:
#                 nazivnik += 1/(udaljenost(xi, cj)**p)
#         rez += brojnik/nazivnik
#         return rez
#
#
#     def membership(p, clusters, cj, xi):
#         brojnik = udaljenost(xi, cj)**(-p-2)
#         nazivnik = 0
#         for c in clusters:
#             nazivnik += udaljenost(xi, c)**(-p-2)
#         return brojnik/nazivnik
#
#
#     def weight(p, clusters, xi):
#         brojnik = 0
#         for c in clusters:
#             brojnik += udaljenost(xi, c)**(-p-2)
#         nazivnik = 0
#         for c in clusters:
#             nazivnik += udaljenost(xi, c)**(-p)
#         nazivnik **= 2
#         return brojnik/nazivnik

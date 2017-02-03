from construct_dataset import PellegMoore, BIRCH
from algorithms import KMeans, FindClusters
import matplotlib.pyplot as plt


# print("First test: KMeans on PellegMoore dataset")
# dataset = PellegMoore()
# initial_centroides = FindClusters.initialize_centroides_forgy(dataset.data_points, len(dataset.centroids))
# solution = KMeans.test_algorithm(2, initial_centroides, dataset.data_points)
#
# plt.plot(dataset.centroids.T[0], dataset.centroids.T[1], 'ro', solution.T[0], solution.T[1], 'bs')
# plt.show()

print("First test: KMeans on BIRCH dataset")
dataset = BIRCH()
initial_centroides = FindClusters.initialize_centroides_forgy(dataset.data_points, len(dataset.centroids))
solution = KMeans.test_algorithm(3, initial_centroides, dataset.data_points)

plt.plot(dataset.centroids.T[0], dataset.centroids.T[1], 'ro', solution.T[0], solution.T[1], 'bs')
plt.show()

dataset.check_true_centroids(solution)

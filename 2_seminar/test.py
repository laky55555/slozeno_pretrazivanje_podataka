from construct_dataset import PellegMoore, BIRCH
from algorithms import KMeans, FindClusters
import matplotlib.pyplot as plt


#print("First test: KMeans on PellegMoore dataset")
dataset = PellegMoore()
# print("First test: KMeans on BIRCH dataset")
#dataset = BIRCH()

initial_centroides = FindClusters.initialize_centroides_forgy(dataset.data_points, len(dataset.centroids))
#initial_centroides = FindClusters.initialize_centroides_random(dataset.data_points, len(dataset.centroids))

# Plot only last graph
# solution = KMeans.test_algorithm(40, initial_centroides, dataset.data_points)
# dataset.check_calculated_centroids(solution)
# plt.figure()
# plt.plot(dataset.centroids.T[0], dataset.centroids.T[1], 'ro', solution.T[0], solution.T[1], 'bs')
# plt.show(block=False)

#Plot all graphs
solution_yield = KMeans.test_algorithm_yield(40, initial_centroides, dataset.data_points)
for i in solution_yield:
    dataset.check_calculated_centroids(i)
    plt.figure()
    plt.plot(dataset.data_points.T[0], dataset.data_points.T[1], 'g^', dataset.centroids.T[0], dataset.centroids.T[1], 'ro', i.T[0], i.T[1], 'bs')
    #plt.plot(dataset.data_points.T[0], dataset.data_points.T[1], 'g^', dataset.centroids.T[0], dataset.centroids.T[1], 'ro')
    plt.show(block=False)

input("Press enter to exit ;)")

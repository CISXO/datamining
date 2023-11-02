"""
Jeong Hyeon Jo

"""

import numpy as np
import time
import random

def matrix_data(data):
    return np.linalg.norm(data[:, np.newaxis] - data, axis=2)

def read_gene_expression_data(filename):
    gene_expression_data = np.genfromtxt(filename, delimiter='\t')
    return gene_expression_data

def init_medoids(distance, k):
    rows = len(distance)

    random_indices = random.sample(range(rows), k)

    medoids = [index for index in random_indices]
    return medoids

def cluster(distance, medoids):
    rows = len(distance)
    clusters = {medoid: [] for medoid in medoids}

    for i in range(rows):
        min_distance = distance[i][medoids[0]]
        closest_medoid = medoids[0]

        for j in medoids:
            if distance[i][j] < min_distance:
                min_distance = distance[i][j]
                closest_medoid = j

        clusters[closest_medoid].append(i)

    return clusters

def calculate_cost(distance, clusters):
    total_cost = 0.0
    for medoid, data_points in clusters.items():
        for data_point in data_points:
            total_cost += distance[medoid][data_point]

    return total_cost

def swap_medoids(clusters, medoids, distance):
    updated = False

    for medoid in medoids:
        for data_point in range(len(distance)):
            if medoid not in clusters or data_point not in clusters[medoid]:
                continue

            new_medoids = medoids.copy()
            new_medoids.remove(medoid)
            new_medoids.append(data_point)

            new_clusters = cluster(distance, new_medoids)
            new_cost = calculate_cost(distance, new_clusters)

            if new_cost < calculate_cost(distance, clusters):
                clusters = new_clusters
                medoids = new_medoids
                updated = True

    return clusters, medoids, updated

def k_medoids(gene, k):
    distance = matrix_data(gene)
    medoids = init_medoids(distance, k)
    clusters = cluster(distance, medoids)

    exist_medoids = medoids.copy()

    prev_cost = calculate_cost(distance, clusters)
    updated = True

    while updated:
        clusters, medoids, updated = swap_medoids(clusters, medoids, distance)
        if updated:
            prev_cost = calculate_cost(distance, clusters)

    return clusters

def write_output_to_file(output_filename, clusters):
    with open(output_filename, 'w') as file:
        for medoid, cluster_data in clusters.items():
            file.write(f"{len(cluster_data)}: ")
            for data_point in cluster_data:
                file.write(f"{data_point} ")
            file.write("\n")

def main():
    input_filename = 'assignment3_input.txt'
    output_filename = 'assignment4_output2.txt'
    gene_expression_data = read_gene_expression_data(input_filename)
    k = 10
    start_time = time.time()
    clusters = k_medoids(gene_expression_data, k)
    write_output_to_file(output_filename, clusters)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed Time: {elapsed_time} seconds")

if __name__ == '__main__':
    main()

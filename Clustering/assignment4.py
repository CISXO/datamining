"""
Jeong Hyeon Jo

"""


import time
import random
import numpy as np

def matrix_data(data):
    distance_matrix = np.linalg.norm(data[:, np.newaxis] - data, axis=2)
    rounded_distance_matrix = np.round(distance_matrix, 3)
    return rounded_distance_matrix


def read_gene_expression_data(filename):
    gene_expression_data = np.genfromtxt(filename, delimiter='\t')
    return gene_expression_data


def init_medoids(distance, k):
    rows = len(distance)

    random_indices = random.sample(range(rows), k)

    medoids = [index for index in random_indices]
    medoids = [261, 257, 164, 306, 270, 108, 242, 432, 341, 396]
    return medoids


def cluster(distance, init_medoid):
    rows = len(distance)
    clusters = {medoid: [] for medoid in init_medoid}
    cur_cost = 0.0

    for i in range(rows):
        min_dist = distance[i][init_medoid[0]]
        closest_medoid = init_medoid[0]

        for j in init_medoid:
            if distance[i][j] < min_dist:
                min_dist = distance[i][j]
                closest_medoid = j

        clusters[closest_medoid].append(i)
        cur_cost += min_dist

    return clusters, round(cur_cost, 3)

# 거리 최소인 값을 리스트로 뽑아주는 함수가 필요
def min_distance(distance, clusters, exist):
    all_distances = []

    for cluster_key, cluster_data in clusters.items():
        for data_point in cluster_data:
            if data_point in exist:
                continue

            dist = distance[cluster_key][data_point]
            all_distances.append((cluster_key, data_point, dist))

    # 한 번만 정렬을 수행하여 최소 거리를 찾음
    all_distances.sort(key=lambda x: x[2])

    return all_distances


# swap 된 경우 exist_update
def swap_medoids(min_list, cost, medoids, distance, existed):
    prev_medoid = medoids[:]
    update_cost = float('inf')
    updated = False
    for key, val, dist in min_list:
        for change in range(len(prev_medoid)):
            if prev_medoid[change] == key:
                prev_medoid[change] = val # medoid 교체
                # cost를 위한 cluster
                cur_cluster, update_cost = cluster(distance, prev_medoid)
                if cost > update_cost:
                    updated = True
                    existed.append(val)

                    return prev_medoid, update_cost, updated, cur_cluster
                else:
                    prev_medoid = medoids[:]

    return prev_medoid, update_cost, updated, cur_cluster


def k_medoids(gene, k):
    distance = matrix_data(gene)
    medoids = init_medoids(distance, k)
    clusters, cost = cluster(distance, medoids)
    exist_medoid = list()
    # 미도이드 체크

    for key in medoids:
        exist_medoid.append(key)

    min_list = min_distance(distance, clusters, exist_medoid)

    update = True

    while update:
        medoids, update_cost, update, cur_clust = swap_medoids(min_list, cost, medoids, distance, exist_medoid)
        cost = update_cost  # 확인
        clusters = cur_clust
        min_list = min_distance(distance, clusters, exist_medoid)
    # clusters = cluster(distance, medoids)

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
    output_filename = 'assignment4_output.txt'
    gene_expression_data = read_gene_expression_data(input_filename)
    k = 10
    start_time = time.time()  # Record the start time
    clusters = k_medoids(gene_expression_data, k)
    write_output_to_file(output_filename, clusters)
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Elapsed Time: {elapsed_time} seconds")


if __name__ == '__main__':
    main()

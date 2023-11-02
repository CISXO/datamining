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
    medoids = [261, 257, 164, 306, 270, 108, 242, 432, 341, 396]
    return medoids


def cluster(distance, init_medoid):
    rows = len(distance)
    clusters = {medoid: [] for medoid in init_medoid}  # 각 init_medoid를 key로 하는 빈 리스트 생성

    for i in range(rows):
        min_dist = distance[i][init_medoid[0]]  # 초기값을 첫 번째 메도이드로 설정
        closest_medoid = init_medoid[0]  # 가장 가까운 메도이드의 인덱스를 저장

        for j in init_medoid:
            if distance[i][j] < min_dist:
                min_dist = distance[i][j]
                closest_medoid = j

        clusters[closest_medoid].append(i)  # 데이터 i를 가장 가까운 메도이드의 클러스터에 추가

    return clusters


def cost_sum(distance, clusters):
    cur_cost = 0.0
    for key, val in clusters.items():
        for dist in val:
            cur_cost += distance[key][dist]

    return round(cur_cost, 3)


# 거리 최소인 값을 리스트로 뽑아주는 함수가 필요
def min_distance(distance, clusters, exist):
    all_distances = []
    for key, val in clusters.items():
        for data_point in val:
            if data_point not in exist:  # Exclude the medoid itself
                dist = distance[key][data_point]
                all_distances.append((key, data_point, dist))

    sorted_distances = sorted(all_distances, key=lambda x: x[2])
    return sorted_distances


# swap 된 경우 exist_update
def swap_medoids(min_list, cost, medoids, distance, existed):
    prev_medoid = medoids[:]
    update_cost = float('inf')
    updated = False
    for key, val, dist in min_list:
        for change in range(len(prev_medoid)):
            if dist ==0:
                continue
            if prev_medoid[change] == key:
                prev_medoid[change] = val
                cur_cluster = cluster(distance, prev_medoid)
                update_cost = cost_sum(distance, cur_cluster)
                if cost > update_cost:
                    updated = True
                    existed.append(val)
                    return prev_medoid, update_cost, updated, cur_cluster
                else:
                    prev_medoid = medoids[:]
    # this_cost
    return prev_medoid, update_cost, updated, cur_cluster


def k_medoids(gene, k):
    distance = matrix_data(gene)
    medoids = init_medoids(distance, k)
    clusters = cluster(distance, medoids)

    exist_medoid = list()
    # 미도이드 체크

    for key in medoids:
        exist_medoid.append(key)
    # 2번
    cost = cost_sum(distance, clusters)  # 확인
    min_list = min_distance(distance, clusters, exist_medoid)

    update = True

    while update:
        medoids, update_cost, update, cur_clust = swap_medoids(min_list, cost, medoids, distance, exist_medoid)
        cost = update_cost  # 확인
        clusters = cur_clust
        min_list = min_distance(distance, clusters, exist_medoid)

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

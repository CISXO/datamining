import numpy as np
import time

#거리를 matrix로 만들어 저장
def matrix_data(data):
    return np.linalg.norm(data[:, np.newaxis] - data, axis=2)

#초기 medoids를 설정하는 함수 10개의 가장 작은 메도이드를 설정
def init_medoids(distance, k):
    rows = len(distance)
    clusted_data= {}
    for i in range(rows):
        sum = 0
        for j in range(rows):
            sum += distance[i][j]
        clusted_data[i] = round(sum, 3)
    sorted_data = sorted(clusted_data.items(), key=lambda x: x[1])

    medoids = [item[0] for item in sorted_data[:k]]

    return medoids

# 각각의 비메도이드에서 k메도이드들간의 거리중 가장 가까운 거리를 클러스터로 설정
def cluster(distance, init_medoid):
    rows = len(distance)
    clusters = {medoid: [] for medoid in init_medoid}

    for i in range(rows):
        min_distance = distance[i][init_medoid[0]]
        closest_medoid = init_medoid[0]

        for j in init_medoid:
            if distance[i][j] < min_distance:
                min_distance = distance[i][j]
                closest_medoid = j

        clusters[closest_medoid].append(i)

    return clusters

#초기 미도이드에서 가장 가까운 거리를 미도이드로 설정하는 함수
def min_medoids(distance, clusters):
    medoids = []

    for key, val in clusters.items():
        min_distance_sum = float('inf')
        medoid_candidate = None

        for i in val:
            distance_sum = 0
            for j in val:
                distance_sum += distance[i][j]

            if distance_sum < min_distance_sum:
                min_distance_sum = distance_sum
                medoid_candidate = i

        medoids.append(medoid_candidate)

    return medoids


def read_gene_expression_data(filename):
    gene_expression_data = np.genfromtxt(filename, delimiter='\t')
    return gene_expression_data

#함수들 조합하는 함수
def k_medoids(gene, k):
    distance = matrix_data(gene)
    medoids = init_medoids(distance, k)
    clusters = cluster(distance, medoids)
    prev_medoids = None

    while prev_medoids != medoids:
        prev_medoids = medoids
        medoids = min_medoids(distance, clusters)
        clusters = cluster(distance, medoids)

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
    output_filename = 'assignment3_output.txt'
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
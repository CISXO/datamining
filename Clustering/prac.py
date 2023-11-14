# 컴퓨터정보통신공학부 조상필_2019253080

import sys
import time
import random
import heapq
import numpy as np
from decimal import Decimal, getcontext
from math import *

def get_input_data(filename):
    input_file = open(filename, 'r')
    data_list = []
    
    for line in input_file:
        data_list.append([float(x) for x in line.strip().split()])
        
    return data_list

# gene_data의 각 object끼리의 거리를 계산하여 저장한 배열을 리턴
def get_all_distance(gene_data):
    n = len(gene_data)
    all_distance = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            distance = int(sqrt(sum(pow(a - b, 2) for a, b in zip(gene_data[i], gene_data[j]))) * 10**3) / 10**3
            all_distance[i][j] = distance
            all_distance[j][i] = distance
            
    return all_distance

def find_near_medoids(distances, medoids):
    
    # 초기 클러스터 구조 설정
    init_cluster = {medoid: [] for medoid in medoids}
    
    # 거리의 총합
    total_distance = 0
    # n-k개의 non_medoid들을 medoid와의 거리순으로 정렬할 리스트
    min_distance_order = []
    
    for i in range(len(distances)):
        
        min_distance = 10000000000
        index = 0
        
        for medoid in medoids:
            if i == medoid:  # 본인인 경우 바로 클러스터에 추가
                index = medoid
                min_distance = 0
                break
            else:
                if distances[i][medoid] < min_distance:
                    min_distance = distances[i][medoid]
                    index = medoid
        init_cluster[index].append((i, min_distance))
        total_distance += min_distance
        
        if i != index:
            min_distance_order.append((min_distance, index, i))
    
    min_distance_order.sort(key=lambda x : x[0])
            
    return init_cluster, total_distance, min_distance_order

def kMedoid(gene_data, k):
    
    # 각 object 끼리의 모든 거리 계산 후 저장
    distances = get_all_distance(gene_data)
    
    # 랜덤하게 k개의 medoids 선택 (k = 10)
    medoids = [261, 257, 164, 306, 270, 108, 242, 432, 341, 396]
    # medoids_memo에 medoids 기록
    medoids_memo = set()
    medoids_memo.update(medoids)
    
    # nonmeoids을 가장 가까운 medoids에 assign
    cluster, total_cost, distances_order = find_near_medoids(distances, medoids)
    
    change = True
    
    while change:
        change = False
        for distance, medoid, non_medoid in distances_order:
            if non_medoid in medoids_memo:
                continue
            
            # total cost 계산
            temp = medoid
            medoids = [non_medoid if x == medoid else x for x in medoids]
            temp_cluster, temp_total_cost, temp_distance_order = find_near_medoids(distances, medoids)
            
            if temp_total_cost < total_cost:
                cluster = temp_cluster
                total_cost = temp_total_cost
                distances_order = temp_distance_order
                medoids_memo.add(non_medoid)
                change = True
                break
            else:
                medoids = [temp if x == non_medoid else x for x in medoids]
    
    return cluster




def output_to_file(filename, cluster):
    file = open(filename, 'w')
    
    for key, item in cluster.items():
        s = str(len(item)) + " : " + ' '.join(str(x[0]) for x in item) + "\n"
        file.write(s)
    
    file.close()    

def main():
    
    input_file = 'assignment3_input.txt'
    output_file_name = "assignment4_output2.txt"
    gene_data = get_input_data(input_file)
    start = time.time()
    result_cluster = kMedoid(gene_data, 10)
    end = time.time()
    
    output_to_file(output_file_name, result_cluster)

    # 수행 시간 출력
    elapsed_time = end - start
    print("수행 시간 : {} microsecond".format(elapsed_time * 1e6))
    

    
if __name__ == '__main__':
    main()
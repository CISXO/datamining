"""

Jeong Hyeon Jo

"""

import sys
import time

def read_data1(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
                line = line.split(':')
                line = line[1]
                data.append(list(map(int, line.strip().split(' '))))
    return data

def read_data2(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            data.append(list(map(float, line.strip().split('\t'))))
    return data

def calculate_clust_set(assignment, ground_truth):
    n = len(ground_truth)
    set_A = [0] * (n * (n - 1) // 2)
    set_B = [0] * (n * (n - 1) // 2)

    index = 0
    for i in range(n):
        for j in range(i + 1, n):
            intersection_count = 0
            union_count = 0

            for cluster in assignment:
                if i in cluster and j in cluster:
                    intersection_count += 1
                if i in cluster or j in cluster:
                    union_count += 1

            set_A[index] = intersection_count / union_count

            if ground_truth[i][0] < 0 or ground_truth[i][0] != ground_truth[j][0]:
                set_B[index] = 0
            else:
                set_B[index] = 1

            index += 1

    return set_A, set_B


def calculate_cluster_validation(jaccard_A, jaccard_B):
    ss, sd, ds = 0, 0, 0

    for number in range(len(jaccard_A) - 1):
        if jaccard_A[number] == 1 and jaccard_B[number] == 1:
            ss += 1
        elif jaccard_A[number] == 1 and jaccard_B[number] == 0:
            sd += 1
        elif jaccard_A[number] == 0 and jaccard_B[number] == 1:
            ds += 1

    val = ss / (ss + sd + ds)

    return val


def main():
    input_filename = sys.argv[1]
    input_filename2 = sys.argv[2]

    assignment = read_data1(input_filename)
    ground_truth = read_data2(input_filename2)
    start_time = time.time()

    set_A, set_B = calculate_clust_set(assignment, ground_truth)
    result = calculate_cluster_validation(set_A, set_B)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("incident matrices: : " + str(result))
    print(elapsed_time)

if __name__ == '__main__':
    main()


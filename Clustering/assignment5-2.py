"""

Jeong Hyeon Jo

"""

import sys
import time
import numpy as np

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
    assignment_set = np.zeros((n, n))
    ground_truth_set = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            intersection_count = 0
            union_count = 0

            for cluster in assignment:
                if i in cluster and j in cluster:
                    intersection_count += 1
                if i in cluster or j in cluster:
                    union_count += 1

            assignment_set[i][j] = assignment_set[j][i] = intersection_count / union_count
            if i == j:
                ground_truth_set[i][j] = 1
            if ground_truth[i][0] < 0 or ground_truth[i][0] != ground_truth[j][0]:
                ground_truth_set[i][j] = ground_truth_set[j][i] = 0
            else:
                ground_truth_set[i][j] = ground_truth_set[j][i] = 1
    return assignment_set, ground_truth_set

# 클러스터는 10개 있으니까 1개의 클러스터씩 반복 수행해서 best_f_measure에 넣는다.
# 그 1개의 best_f_measure에서 가장 큰 f-measure를 찾아서 f_score에 넣어준다.
#그렇게 10번 반복하면 f_score 10개가 나오고 그 10개의 평균값을 내주면 된다.
#값이 두번째 ..... 10개의 f-score이 나온다. 10개가 나오면 평균을 한다.
def calculate_f_measure(assignment, assignment_set, ground_truth_set):
    f_score = []  # F-측정값을 저장할 리스트
    fill = False
    for cluster in assignment:
        best_f_measure = 0.0
        for index in cluster:
            #각각의 클러스터안의 오브젝트가 나옴
            #cluster index 하나와 ground_truth간의 정밀도와 재현율을 계산해야 한다.
            common_points = [min(a, b) for a, b in zip(assignment_set[index], ground_truth_set[index]) if
                             a != 0 and b != 0]
            seted_A = [x for x in assignment_set[index] if x != 0]
            seted_B = [y for y in ground_truth_set[index] if y != 0]

            if(len(seted_B) == 0 or len(seted_A) == 0):
                pass
            else:
                precision = len(common_points) / len(seted_A)
                recall = len(common_points) / len(seted_B)
                # F-측정 계산
                if precision + recall > 0:
                    f = (2 * recall * precision) / (recall + precision)
                    best_f_measure = max(best_f_measure, f)
        f_score.append(best_f_measure)

    # 모든 클러스터링 결과에 대한 평균 F-측정 계산
    average_f_measure = sum(f_score) / len(f_score)

    return average_f_measure

def main():
    input_filename = sys.argv[1]
    input_filename2 = sys.argv[2]

    assignment = read_data1(input_filename)
    ground_truth = read_data2(input_filename2)
    start_time = time.time()

    assignment_set, ground_truth_set = calculate_clust_set(assignment, ground_truth)
    result = calculate_f_measure(assignment, assignment_set, ground_truth_set)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("incident matrices: : " + str(result))
    print(elapsed_time)

if __name__ == '__main__':
    main()



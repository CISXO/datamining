"""
Jeong Hyeon Jo

"""

from math import ceil
from itertools import combinations

MIN_SUPPORT = 0.035
# 이 함수는 파일 이름 아래의 파일을 읽고 모든 트랜잭션과 고유한 항목 집합을 추출합니다.
# 파라미터 파일 이름: 입력 파일의 이름(필요한 경우 경로를 제공해야 함)
# return: 트랜잭션 및 고유 항목 세트의 딕셔너리입니다.
def get_input_data(filename):
    input_file = open(filename, 'r')
    transactions = dict()
    itemset = set()
    for line in input_file:
        splitted = line.split()
        trans_id = splitted[0]
        trans_items = splitted[1:]
        transactions[trans_id] = trans_items
        itemset.update(trans_items)
    return transactions, itemset

# 이 함수는 트랜잭션에서 항목 집합의 지원을 계산합니다.
# 매개변수 트랜잭션에서 항목 집합 지원을 계산합니다: 사전의 모든 트랜잭션
# 파라미터 항목 집합: 지원을 계산할 항목 집합
# 반환합니다: 항목 집합의 지원 횟수
def support(transactions, itemset):
    support_count = 0

    for trans_items in transactions.values():
        if itemset.issubset(trans_items):
            support_count += 1

    return support_count

# 이 함수는 크기 (itemset_size - 1)의 빈번한 항목 집합에서 조합을 생성하고
# (itemset_size - 2) 항목을 공유하는 경우 결합된 항목 집합을 허용합니다.
# 매개변수 frequent_itemsets: 발견된 빈번한 항목 집합의 테이블
# 매개변수 itemset_size: 조인된 아이템 셋의 크기
# return: 모든 유효한 조인된 아이템 셋
def generate_selectively_joined_itemsets(frequent_itemsets, itemset_size):
    # seen_itemsets = set()
    joined_itemsets = set()

    for itemset1 in frequent_itemsets[itemset_size - 1]:
        for itemset2 in frequent_itemsets[itemset_size - 1]:
            if itemset1 != itemset2:
                joined_itemset = itemset1.union(itemset2)
                if len(joined_itemset) == itemset_size:
                    joined_itemsets.add(joined_itemset)

    return joined_itemsets


# 이 함수는 선택한 항목 집합의 모든 하위 집합이 모두 빈번한지 여부를 확인하고
# 하위 집합 중 빈번하지 않은 항목 집합이 있으면 항목 집합을 잘라냅니다.
# 매개변수 selected_itemsets: 검사해야 할 항목 집합
# 파라미터 빈번한_아이템셋: 발견된 빈번한 항목 집합의 테이블
# 파라미터 itemset_size: 의도한 빈번한 항목 집합의 크기
# return: 모든 하위 집합이 빈번한 항목 세트
def apply_apriori_pruning(selected_itemsets, frequent_itemsets, itemset_size):
    apriori_pruned_itemsets = set()

    for itemset in selected_itemsets:
        is_frequent = True
        for subset in combinations(itemset, itemset_size - 1):
            if frozenset(subset) not in frequent_itemsets[itemset_size - 1]:
                is_frequent = False
                break
        if is_frequent:
            apriori_pruned_itemsets.add(itemset)

    return apriori_pruned_itemsets

# 이 함수는 선택적 조인 및 사전 가지치기를 통해 # 선택된 모든 하위 집합을 확인하여 크기(itemset_size)의 후보 항목 집합을 생성합니다.
# 매개변수 frequent_itemsets: 발견된 빈번한 항목 집합의 테이블
# param itemset_size: 의도된 빈번한 항목 집합의 크기
# 반환: 선택적 조인 및 선험적 가지치기로 형성된 후보 항목 집합
def generate_candidate_itemsets(frequent_itemsets, itemset_size):
    joined_itemsets = generate_selectively_joined_itemsets(frequent_itemsets, itemset_size)
    candidate_itemsets = apply_apriori_pruning(joined_itemsets, frequent_itemsets, itemset_size)
    return candidate_itemsets

# 이 함수는 주어진 최소 지원을 기반으로 트랜잭션에서 모든 빈번한 항목이 포함된 항목 집합 테이블을 생성합니다.
# 매개변수 트랜잭션을 기반으로 모든 빈번한 항목이 포함된 항목 집합 테이블을 생성합니다: 지원 계산의 기준이 되는 트랜잭션입니다.
# 파라미터 항목: 트랜잭션에 존재하는 고유한 항목 세트
# param min_sup: 빈번한 항목 집합을 찾기 위한 최소 지원
# return: 크기가 다른 모든 빈번한 항목 집합의 테이블
def generate_all_frequent_itemsets(transactions, items, min_sup):
    frequent_itemsets = dict()
    itemset_size = 0
    frequent_itemsets[itemset_size]=[frozenset()]  # Initialize with an empty itemset

    # Frequent itemsets of size 1
    itemset_size += 1
    frequent_itemsets[itemset_size] = list()

    for item in items:
        itemset = frozenset([item])
        itemset_support = support(transactions, itemset)
        if itemset_support >= min_sup:
            frequent_itemsets[itemset_size].append(itemset)

    # Frequent itemsets of greater size
    itemset_size += 1

    while frequent_itemsets[itemset_size - 1]:
        frequent_itemsets[itemset_size] = list()
        candidate_itemsets = generate_candidate_itemsets(frequent_itemsets, itemset_size)
        pruned_itemset = set()

        for itemset in candidate_itemsets:
            itemset_support = support(transactions, itemset)
            if itemset_support >= min_sup:
                pruned_itemset.add(itemset)

        frequent_itemsets[itemset_size] = pruned_itemset
        itemset_size += 1

    return frequent_itemsets
# 이 함수는 모든 빈번한 항목 집합과 해당 지원을 지정된 파일명으로 출력 파일에 기록합니다.
# 파라미터 파일명: 출력 파일의 이름입니다.
# 파라미터 빈번한_아이템셋_테이블: 모든 빈번한 항목 집합을 포함하는 사전
# 파라미터 트랜잭션: 빈번한 항목 집합을 찾은 트랜잭션입니다.
# 반환: void
def output_to_file(filename, frequent_itemsets_table, transactions):
    file = open(filename, 'w')
    for itemset_size in frequent_itemsets_table:

        # Do not print frequent itemsets of size 0 or 1
        if itemset_size == 0:
            continue
        if itemset_size == 1:
            continue

        # Print frequent itemsets of size 2 or larger
        for freq_itemset in frequent_itemsets_table[itemset_size]:
            support_percent = (support(transactions, freq_itemset) / len(transactions)) * 100
            file.write('{0} {1:.2f}% support\n'.format(freq_itemset, support_percent))
    file.close()


# The main function
def main():
    input_filename = 'assignment1_input.txt'
    output_filename = 'assignment1_output.txt'
    cellular_functions, genes_set = get_input_data(input_filename)
    min_sup = ceil(MIN_SUPPORT * len(cellular_functions))
    frequent_itemsets_table = generate_all_frequent_itemsets(cellular_functions, genes_set, min_sup)
    output_to_file(output_filename, frequent_itemsets_table, cellular_functions)

if __name__ == '__main__':
    main()


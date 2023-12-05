"""
Jeong Hyeon Jo
"""
from itertools import combinations
import sys
import time


def data_input(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    items = []
    for line in lines:
        columns = line.strip().split('\t')
        gene_values = ['gene{} {}'.format(i - 1, value.lower()) for i, value in enumerate(columns[1:-1], start=1)]
        disease = columns[-1]
        itemset = set(gene_values) | {disease}
        items.append(itemset)
    return items


def count_itemsets(items, itemset):
    count = 0
    for s in items:
        if itemset.issubset(s):
            count += 1

    return count


def generate_k_items(current_items, k):
    result = []
    for key1, val1 in enumerate(current_items):
        for key2, val2 in enumerate(current_items):
            if key1 == key2:
                continue
            if key1 > key2:
                continue
            union_result = val1.union(val2)
            if len(union_result) == k:
                result.append(union_result)
    return result

def gene_rules(items, frequent_items, min_confidence):
    rules = []
    diseases = {'BreastCancer', 'ColonCancer'}
    for itemset, support in frequent_items.items():
        itemset = set(itemset)
        for size in range(1, len(itemset)):
            for comb in combinations(itemset, size):
                comb_set = set(comb)
                T_set = itemset - comb_set
                if not T_set.isdisjoint(diseases):
                    rules.append((comb_set, T_set, support))
    filtered_rules = calculate_confidence(items, rules, min_confidence)

    return filtered_rules

def calculate_confidence(items, rules, min_confidence):
    filtered_rules = []

    for rule in rules:
        comb_set, T_set, support = rule
        comb_count = count_itemsets(items, comb_set)
        confidence = support / (comb_count / len(items))

        if confidence >= min_confidence:
            filtered_rules.append((comb_set, T_set, support, confidence))

    return filtered_rules

def filter_datas_items(items, k_items, min_support, num):
    datas_items = {}

    for itemset in k_items:
        count = count_itemsets(items, itemset)
        support = count / num

        if support >= min_support:
            datas_items[tuple(sorted(itemset))] = support

    return datas_items

def apriori_frequent_items(items, min_support):
    frequent_items = {}
    num = len(items)
    f_item_counts = {}
    f_items = set()

    for itemset in items:
        for item in itemset:
            current_count = f_item_counts.get(item, 0)
            f_item_counts[item] = current_count + 1

    for item, count in f_item_counts.items():
        if count / num >= min_support:
            f_items.add(item)

    current_items = [{item} for item in f_items]

    while current_items:
        k_items = generate_k_items(current_items, len(current_items[0]) + 1)
        datas = filter_datas_items(items, k_items, min_support, num)
        if not datas:
            break
        frequent_items.update(datas)
        current_items = [set(itemset) for itemset in datas]
    return frequent_items




def output_file(filename, rules):
    with open(filename, 'w') as file:
        for gene_set, outcome_set, support, confidence in rules:
            if len(gene_set) >= 2:
                gene_str = ', '.join(gene_set)
                outcome_str = ', '.join(outcome_set)
                support_percent = support * 100
                confidence_percent = confidence * 100
                output_line = f"{{{gene_str}}} → {{{outcome_str}}}: {support_percent:.2f}% support, {confidence_percent:.2f}% confidence\n"
                file.write(output_line)
    return 0


def main():
    file_name = sys.argv[1]
    min_support = 0.30
    min_confidence = 0.60
    start = time.time()

    items = data_input(file_name)
    frequent_items = apriori_frequent_items(items, min_support)
    rules = gene_rules(items, frequent_items, min_confidence)

    output_name = 'assignment8_output.txt'
    output_file(output_name, rules)

    end = time.time()
    elapsed_time = end - start
    print("수행 시간 : {} microsecond".format(elapsed_time * 1e6))


if __name__ == "__main__":
    main()

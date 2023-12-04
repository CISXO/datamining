from itertools import combinations
import sys
import time


def data_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    items = []
    for line in lines:
        columns = line.strip().split('\t')
        gene_values = ['gene{} {}'.format(i - 1, value.lower()) for i, value in enumerate(columns[1:-1], start=1)]
        disease = columns[-1]
        itemset = set(gene_values) | {disease}
        items.append(itemset)
    return items


def apori_frequent_items(items, min_support):
    frequent_items = {}
    num = len(items)
    f_item_counts = {}
    for itemset in items:
        for item in itemset:
            f_item_counts[item] = f_item_counts.get(item, 0) + 1
    f_items = set()
    for item, count in f_item_counts.items():
        if count / num >= min_support:
            f_items.add(item)
    current_items = [{item} for item in f_items]

    k = 2
    while current_items:
        k_items = []
        valid = {}

        for i in current_items:
            for j in current_items:
                if len(i.union(j)) == k:
                    k_items.append(i.union(j))

        for itemset in k_items:
            count = sum(1 for s in items if itemset.issubset(s))
            if count / num >= min_support:
                valid[tuple(sorted(itemset))] = count / num

        if not valid:
            break
        frequent_items.update(valid)
        current_items = [set(itemset) for itemset in valid]
        k += 1

    return frequent_items


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
                    comb_count = sum(1 for s in items if comb_set.issubset(s))
                    confidence = support / (comb_count / len(items))
                    if confidence >= min_confidence:
                        rules.append((comb_set, T_set, support, confidence))
    return rules


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
    file_path = sys.argv[1]
    min_support = 0.30
    min_confidence = 0.60
    start = time.time()

    items = data_input(file_path)
    frequent_items = apori_frequent_items(items, min_support)
    rules = gene_rules(items, frequent_items, min_confidence)

    output_name = 'assignment8_output.txt'
    output_file(output_name, rules)

    end = time.time()
    elapsed_time = end - start
    print("수행 시간 : {} microsecond".format(elapsed_time * 1e6))


if __name__ == "__main__":
    main()

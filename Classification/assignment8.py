from math import ceil
from itertools import combinations

MIN_SUPPORT = 0.3

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

def support(transactions, itemset):
    support_count = 0
    for trans_items in transactions.values():
        if itemset.issubset(trans_items):
            support_count += 1
    return support_count

def generate_selectively_joined_itemsets(frequent_itemsets, itemset_size):
    joined_itemsets = set()
    for itemset1 in frequent_itemsets[itemset_size - 1]:
        for itemset2 in frequent_itemsets[itemset_size - 1]:
            if itemset1 != itemset2:
                joined_itemset = itemset1.union(itemset2)
                if len(joined_itemset) == itemset_size:
                    joined_itemsets.add(joined_itemset)
    return joined_itemsets

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

def generate_candidate_itemsets(frequent_itemsets, itemset_size):
    joined_itemsets = generate_selectively_joined_itemsets(frequent_itemsets, itemset_size)
    candidate_itemsets = apply_apriori_pruning(joined_itemsets, frequent_itemsets, itemset_size)
    return candidate_itemsets

def generate_all_frequent_itemsets(transactions, items, min_sup):
    frequent_itemsets = dict()
    itemset_size = 0
    frequent_itemsets[itemset_size] = [frozenset()]  # Initialize with an empty itemset

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

def generate_association_rules(frequent_itemsets, transactions, min_confidence):
    rules = []

    for itemset_size in frequent_itemsets:
        if itemset_size < 2:
            continue

        for freq_itemset in frequent_itemsets[itemset_size]:
            for i in range(1, itemset_size):
                for antecedent in combinations(freq_itemset, i):
                    antecedent_set = frozenset(antecedent)
                    consequent_set = freq_itemset - antecedent_set

                    support_antecedent = support(transactions, antecedent_set)
                    support_itemset = support(transactions, freq_itemset)

                    confidence = support_itemset / support_antecedent

                    if confidence >= min_confidence:
                        rule = {
                            "antecedent": antecedent_set,
                            "consequent": consequent_set,
                            "support": support_itemset,
                            "confidence": confidence
                        }
                        rules.append(rule)

    return rules

def output_rules_to_file(filename, rules):
    with open(filename, 'w') as file:
        for rule in rules:
            file.write(f'{rule["antecedent"]} → {rule["consequent"]}: '
                       f'{rule["support"]}% support, {rule["confidence"]*100}% confidence\n')

def main():
    input_filename = 'dataset.txt'
    output_filename = 'assignment8_output.txt'
    cellular_functions, genes_set = get_input_data(input_filename)

    # Find frequent itemsets with 30% minimum support
    min_sup = ceil(MIN_SUPPORT * len(cellular_functions))
    frequent_itemsets_table = generate_all_frequent_itemsets(cellular_functions, genes_set, min_sup)

    # Find association rules with 60% minimum confidence
    min_confidence = 0.6
    rules = generate_association_rules(frequent_itemsets_table, cellular_functions, min_confidence)

    # Output rules to a file
    output_rules_to_file(output_filename, rules)

if __name__ == '__main__':
    main()

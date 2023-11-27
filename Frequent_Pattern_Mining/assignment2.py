"""
Jeong Hyeon Jo
"""

from math import ceil

MIN_SUPPORT_PERCENT = 0.035


# This function reads a file under filenames and extracts all transactions and a set of distinct items
# param filename: The name of the input file
# return: A dictionary of transactions and set of distinct items
def get_input_data(filename):
    input_file = open(filename, 'r')
    transaction = dict()
    genes_set = set()

    for line in input_file:
        # add to dictionary from each line
        # dictionary keys: transaction ID(first column)
        # dictionary values: genes
        sp = line.strip().split('\t')
        transaction[sp[0]] = set(sp[1:])

        # add genes to genes_set
        genes_set.update(sp[1:])

    return transaction, genes_set


# This function computes the frequency of union set and prunes the non-closed branch for each itemset pair
# param frequent_itemsets: The table of frequent closed itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: merged itemsets which non-closed branches are removed
def apply_charm_algorithm(frequent_closed_itemsets, itemset_size):
    copied = frequent_closed_itemsets[itemset_size - 1].copy()
    merged_itemsets = list()
    seen_itemsets = set()
    same_tid = list()
    for i, item1 in enumerate(copied):
        for j, item2 in enumerate(copied):
            if i >= j:
                continue
            key1, val1 = item1
            key2, val2 = item2

            key = frozenset(key1.union(key2))
            val = val1.intersection(val2)

            deletet_id = list()
            if  key not in seen_itemsets and len(key) == itemset_size:
                seen_itemsets.add(key)
                merged_itemsets.append((key, val))
                # 1 t(x1) = t(x2) prun 1 or 2
                if val1 == val2:
                    for tid_key, tid_val in frequent_closed_itemsets[itemset_size - 1]:
                        if tid_val != val2:
                            deletet_id.append((tid_key, tid_val))
                    frequent_closed_itemsets[itemset_size - 1] = deletet_id
                # 2 t(x1) < t(x2) prun 1
                elif val1.issubset(val2):
                    for tid_key, tid_val in frequent_closed_itemsets[itemset_size - 1]:
                        if tid_val != val2:
                            deletet_id.append((tid_key, tid_val))
                    frequent_closed_itemsets[itemset_size - 1] = deletet_id
                # 3 t(x1) > t(x2) prun 2
                elif val2.issubset(val1):
                    for tid_key, tid_val in frequent_closed_itemsets[itemset_size - 1]:
                        if tid_val != val1:
                            deletet_id.append((tid_key, tid_val))
                    frequent_closed_itemsets[itemset_size - 1] = deletet_id
                # 4 t(x1) != t(x2)  keep

    # for i in sorted(same_tid, reverse=True):
    #     frequent_closed_itemsets[itemset_size - 1].pop(i)

    return merged_itemsets


# This function prunes merged_itemset if support is smaller than min_support
# param merged_itemsets: The list of merged itemset
# param min_support: The minimum support to find frequent itemsets
# return: frequent itemsets
def pruning_infrequenct_itemsets(merged_itemsets, min_support):
    pruned_itemsets = list()
    for key, val in merged_itemsets:
        if len(val) >= min_support:
            pruned_itemsets.append((key, val))

    return pruned_itemsets


# This function generates a table of closed itemsets with all frequent items from transactions
# param transactions: The transactions based upon which support is calculated
# param items: The unique set of items present in the transaction
# param min_support: The minimum support to find frequent itemsets
# return: The table of all frequent closed itemsets of different sizes
def generate_all_frequent_closed_itemsets(transactions, items, min_support):
    frequent_closed_itemsets = dict()

    itemset_size = 0
    frequent_closed_itemsets[itemset_size] = list()
    frequent_closed_itemsets[itemset_size].append(frozenset())

    # Frequent itemsets of size 1
    itemset_size += 1
    frequent_closed_itemsets[itemset_size] = list()

    for item in items:
        tid_id = []
        for key, val in transactions.items():
            if item in val:
                tid_id.append(key)
        if len(tid_id) >= min_support:
            frequent_closed_itemsets[itemset_size].append((frozenset([item]), set(tid_id)))

    # Frequent itemsets of greater size
    itemset_size += 1

    while frequent_closed_itemsets[itemset_size - 1]:
        frequent_closed_itemsets[itemset_size] = list()

        # get merged_itemsets by using charm algorithm
        merged_itemsets = apply_charm_algorithm(frequent_closed_itemsets, itemset_size)

        # if support is greater than min_support then add to pruned_itemsets
        pruned_itemsets = pruning_infrequenct_itemsets(merged_itemsets, min_support)

        # add pruned_itemsets to frequent_closed_itemsets
        frequent_closed_itemsets[itemset_size] = pruned_itemsets

        itemset_size += 1

    return frequent_closed_itemsets


# This function writes all frequent closed itemsets along with their support to the output file with the given filename
# param filename: The name for the output file
# param frequent_closed_itemsets_table: The dictionary which contains all frequent closed itemsets
# param transactions: The transactions from which the frequent itemsets are found
# return: void
def output_to_file(filename, frequent_closed_itemsets_table, transactions):
    file = open(filename, 'w')

    for dic_k, dic_v in frequent_closed_itemsets_table.items():
        # skip if the size of sets is smaller than 2
        if dic_k < 2:
            continue
        for item in dic_v:
            s = str(item[0])[10:-1] + " " + str(round(len(item[1]) / len(transactions) * 100, 2)) + " % support\n"
            file.write(s)
    file.close()


# The main function
def main():
    input_filename = 'assignment1_input.txt'
    output_filename = 'result.txt'
    cellular_functions, genes_set = get_input_data(input_filename)
    min_support = ceil(MIN_SUPPORT_PERCENT * len(cellular_functions))
    frequent_closed_itemsets_table = generate_all_frequent_closed_itemsets(cellular_functions, genes_set, min_support)
    output_to_file(output_filename, frequent_closed_itemsets_table, cellular_functions)


if __name__ == '__main__':
    main()

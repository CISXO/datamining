from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


# Read the gene expression data from the tab-delimited text file
def read_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(line.strip().split('\t'))
    return data


# Find frequent gene-expression/disease sets using the Apriori-like algorithm
def find_frequent_sets(data, min_support):
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    frequent_sets = apriori(df, min_support=min_support, use_colnames=True)

    return frequent_sets


# Find association rules with a minimum confidence
def find_association_rules(frequent_sets, min_confidence):
    rules = association_rules(frequent_sets, metric="confidence", min_threshold=min_confidence)

    return rules


# Filter and print rules with at least two genes in the condition
def print_rules(rules, output_file):
    with open(output_file, 'w') as file:
        for index, row in rules.iterrows():
            antecedents = row['antecedents']
            if len(antecedents) >= 2:
                file.write(
                    f"{set(antecedents)} → {set(row['consequents'])}: {row['support'] * 100:.2f}% support, {row['confidence'] * 100:.2f}% confidence\n")


if __name__ == "__main__":
    import pandas as pd

    # Provide the path to your gene expression data file
    data_file_path = "dataset.txt"

    # Minimum support and confidence thresholds
    min_support = 0.3
    min_confidence = 0.6

    # Read data
    gene_data = read_data(data_file_path)

    # Find frequent gene-expression/disease sets
    frequent_sets = find_frequent_sets(gene_data, min_support)

    # Find association rules
    rules = find_association_rules(frequent_sets, min_confidence)

    # Print rules with at least two genes in the condition
    output_file_path = "output_rules.txt"
    print_rules(rules, output_file_path)

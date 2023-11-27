# txt파일의 중복된 데이터 있는지 확인하는 test 코드
def get_input_data(filename):
    with open(filename, 'r') as input_file:
        data = [line.strip() for line in input_file]

    return data

def find_duplicates_in_dataset(data):
    all_genes = set()
    duplicates = set()

    for group in data:
        gene_counts = group.split(': ')[1].split(' ')
        for gene_count in gene_counts:
            gene = gene_count.split(' ')[0]
            if gene in all_genes:
                duplicates.add(gene)
            else:
                all_genes.add(gene)

    return duplicates

filename = 'example1.txt'
data = get_input_data(filename)
result = find_duplicates_in_dataset(data)

if result:
    print(f"The following genes are duplicated across the entire dataset: {', '.join(result)}")
else:
    print("There are no duplicated genes in the dataset.")

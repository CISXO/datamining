"""
Jeong Hyeon Jo

"""
import copy
import sys
import time


def get_input_data(filename):
    with open(filename, 'r') as input_file:
        graph_set = []

        for line in input_file:
            val1, val2 = line.strip().split('\t')

            found_graphs = []
            for graph in graph_set:
                if val1 in graph[0] or val2 in graph[0]:
                    found_graphs.append(graph)

            if not found_graphs:
                new_graph = ({val1, val2}, {(val1, val2)})
                graph_set.append(new_graph)
            elif len(found_graphs) == 1:
                found_graph = found_graphs[0]
                found_graph[0].update({val1, val2})
                found_graph[1].add((val1, val2))
            else:
                merged_nodes = {val1, val2}
                merged_edges = {(val1, val2)}
                for found_graph in found_graphs:
                    merged_nodes.update(found_graph[0])
                    merged_edges.update(found_graph[1])
                    graph_set.remove(found_graph)
                graph_set.append((merged_nodes, merged_edges))

    return graph_set


def density_calculate(sub_graph):
    node = len(sub_graph[0])
    edge = len(sub_graph[1])
    density = (edge * 2) / (node * (node - 1))
    return density >= 0.4


def Jaccard_index(graph):
    minimum_list = []
    for node1, node2 in graph[1]:
        x = set()
        y = set()
        for edges in graph[1]:
            if node1 in edges:
                x.add(edges[0])
                x.add(edges[1])
            if node2 in edges:
                y.add(edges[0])
                y.add(edges[1])
        if x:
            x.remove(node1)
        if y:
            y.remove(node2)

        # 한번 체크 엣지 반복 제대로 되었는지
        intersection = len(x.intersection(y))
        union = len(x.union(y))
        jaccard_index = intersection / union
        if node1 < node2:
            minimum_list.append((node1, node2, jaccard_index))
        else:
            minimum_list.append((node2, node1, jaccard_index))
        # jaccard_index를 기준으로 정렬
    sorted_jaccard_list = sorted(minimum_list, key=lambda x: (x[2], tuple(sorted([x[0], x[1]]))), reverse=True)
    sorted_jaccard_list = [item for item in sorted_jaccard_list if item[2] > 0.1]
    sorted_jaccard_list = [(item[0], item[1]) for item in sorted_jaccard_list]
    return sorted_jaccard_list if len(sorted_jaccard_list) > 9 else None

def extract_edges(graph, selected_nodes):
    selected_edges = set()

    for edge in graph:
        if edge[0] in selected_nodes and edge[1] in selected_nodes:
            selected_edges.add(edge)

    return selected_edges

def create_graph(sub_graph):
    sub_set = []
    density = True
    for sub in sub_graph:
        val1, val2 = sub

        found_graphs = []
        for graph in sub_set:
            if val1 in graph[0] or val2 in graph[0]:
                found_graphs.append(graph)

        if not found_graphs:
            new_graph = ({val1, val2}, {(val1, val2)})
            sub_set.append(new_graph)
        elif len(found_graphs) == 1:
            check_graph = copy.deepcopy(found_graphs[0])
            check_graph[0].update({val1, val2})
            selected_edges = extract_edges(sub_graph, check_graph[0])
            density = density_calculate((check_graph[0], selected_edges))
            if density:
                found_graph = found_graphs[0]
                found_graph[0].update({val1, val2})
                found_graph[1].add((val1, val2))
            else:
                continue
        else:
            merged_nodes = {val1, val2}
            merged_edges = {(val1, val2)}
            for found_graph in found_graphs:
                merged_nodes.update(found_graph[0])
                merged_edges.update(found_graph[1])
            selected_edges = extract_edges(sub_graph, merged_nodes)
            density = density_calculate((merged_nodes, selected_edges))
            if density:
                for found_graph in found_graphs:
                    sub_set.remove(found_graph)

                sub_set.append((merged_nodes, merged_edges))
            else:
                continue

    return sub_set

def Bottom_up(Graph_set):
    clusters_set = set() # set을 초기화
    sub_list = []
    for graph in Graph_set:
        Complete_clust = None  # Initialize before the loop

        sub_graph = Jaccard_index(graph)

        if sub_graph:
            Complete_clust = create_graph(sub_graph)
        if Complete_clust:
            for complete in Complete_clust:
                if len(complete[0]) > 9:
                    clusters_set.add(tuple(complete[0]))
    return clusters_set


def Sorted_cluster(cluster, filename):
    sorted_cluster = sorted(cluster, key=lambda x: len(x), reverse=True)
    printed_graphs = set()

    with open(filename, 'w') as file:
        for graph in sorted_cluster:
            if graph not in printed_graphs:
                file.write(f"{len(graph)}: {' '.join(graph)}\n")
                printed_graphs.add(graph)
    return 0

def main():
    input_filename = sys.argv[1]
    output_filename = 'assignment7_output.txt'
    start_time = time.time()  # Record the start time
    Graph_set = get_input_data(input_filename)

    completed = Bottom_up(Graph_set)

    Sorted_cluster(completed, output_filename)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print("수행 시간 : {} microsecond".format(elapsed_time * 1e6))


if __name__ == '__main__':
    main()

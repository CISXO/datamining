"""
Jeong Hyeon Jo

"""

import time
from collections import deque


def get_input_data(filename):
    with open(filename, 'r') as input_file:
        graph_set = []

        for line in input_file:
            val1, val2 = line.strip().split('\t')

            # Find the graph that contains either val1 or val2
            found_graphs = []
            for graph in graph_set:
                if val1 in graph[0] or val2 in graph[0]:
                    found_graphs.append(graph)

            # If both nodes are not found in any existing graph, create a new graph
            if not found_graphs:
                new_graph = ({val1, val2}, {(val1, val2)})
                graph_set.append(new_graph)
            elif len(found_graphs) == 1:
                # If both nodes are found in the same graph, update the graph
                found_graph = found_graphs[0]
                found_graph[0].update({val1, val2})
                found_graph[1].add((val1, val2))
            else:
                # If both nodes are found in different graphs, merge the graphs
                merged_nodes = {val1, val2}
                merged_edges = {(val1, val2)}
                for found_graph in found_graphs:
                    merged_nodes.update(found_graph[0])
                    merged_edges.update(found_graph[1])
                    graph_set.remove(found_graph)
                graph_set.append((merged_nodes, merged_edges))

    return graph_set


def density_calculate(sub_graph, weight):
    node = len(sub_graph[0])
    edge = len(sub_graph[1])
    density = (edge * 2) / (node * (node - 1))
    if density < weight:
        return Jaccard_index(sub_graph)
    else:
        return sub_graph


def Jaccard_index(graph):
    minimum_list = []
    weight = 0.4
    global cluster_set
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
    sorted_jaccard_list = sorted(minimum_list, key=lambda x: (x[2], tuple(sorted([x[0], x[1]]))))

    # sorted_jaccard_list = [(item[0], item[1]) for item in sorted_jaccard_list]
    if len(sorted_jaccard_list)>10:
        return sorted_jaccard_list

def Bottom_up(Graph_set):
    clusters_set = set()  # set을 초기화
    for graph in Graph_set:
        sub_graph = Jaccard_index(graph)

        Complete_clust = sub_graph
        if Complete_clust:
            for val in Complete_clust:
                clusters_set.add(tuple(val)) # set에 값을 추가
    return clusters_set

def bfs(graph):
    if not graph:
        return False  # 그래프가 비어있으면 연결되지 않은 것으로 간주

    visited = set()
    start_node = next(iter(graph))[0]  # 그래프에서 첫 번째 노드를 시작 노드로 설정
    queue = deque([start_node])
    visited.add(start_node)

    while queue:
        current_node = queue.popleft()

        for edge in graph:
            if current_node in edge:
                neighbor = edge[0] if edge[1] == current_node else edge[1]
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)

    # 그래프의 모든 노드가 방문되었는지 확인
    all_nodes = set(node for edge in graph for node in edge)
    return len(visited) == len(all_nodes)


def Sorted_cluster(cluster, filename):
    sorted_cluster = sorted(cluster, key=lambda x: len(x), reverse=True)
    printed_graphs = set()

    with open(filename, 'w') as file:
        for graph in sorted_cluster:
            if graph not in printed_graphs:
                file.write(f"{len(graph)}: {' '.join(graph)}\n")
                printed_graphs.add(graph)

    return 0

cluster_set = []
def main():
    input_filename = 'example.txt'
    output_filename = 'example1.txt'
    start_time = time.time()  # Record the start time
    Graph_set = get_input_data(input_filename)

    completed = Bottom_up(Graph_set)

    Sorted_cluster(completed, output_filename)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print("수행 시간 : {} microsecond".format(elapsed_time * 1e6))


if __name__ == '__main__':
    main()

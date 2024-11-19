import json
from collections import defaultdict
import networkx as nx


# Função para carregar arquivos JSON
def load_graph_files(adjacency_list_file, edge_weights_file):
    with open(adjacency_list_file, "r") as adj_file:
        adj_list = json.load(adj_file)
    with open(edge_weights_file, "r") as weights_file:
        edge_weights = json.load(weights_file)
    return adj_list, edge_weights


# Função para transformar um grafo em Euleriano
def make_eulerian(adj_list, edge_weights):
    degrees = defaultdict(int)

    # Calcula os graus dos vértices
    for u in adj_list:
        for v in adj_list[u]:
            degrees[u] += 1
            degrees[v] += 1

    # Identifica vértices de grau ímpar
    odd_vertices = [v for v in degrees if degrees[v] % 2 == 1]
    added_edges = []

    # Emparelhar vértices ímpares com menores custos
    while odd_vertices:
        v = odd_vertices.pop()
        closest, min_cost = None, float('inf')

        for u in odd_vertices:
            edge = f"{min(str(v), str(u))}-{max(str(v), str(u))}"  # Convertendo para string
            cost = edge_weights.get(edge, float('inf'))  # Usando .get() para evitar KeyError
            if cost < min_cost:
                closest, min_cost = u, cost

        # Verifica se 'closest' está na lista antes de removê-lo
        if closest in odd_vertices:
            odd_vertices.remove(closest)
            adj_list[str(v)].append(str(closest))  # Garantir que as chaves sejam strings
            adj_list[str(closest)].append(str(v))  # Garantir que as chaves sejam strings
            edge = f"{min(str(v), str(closest))}-{max(str(v), str(closest))}"
            edge_weights[edge] = min_cost
            added_edges.append(edge)

    return added_edges


# Função para construir o grafo de fluxo
def build_flow_graph(adj_list, edge_weights, num_agents):
    G = nx.DiGraph()

    # Adiciona vértices
    for u in adj_list:
        G.add_node(u)

    # Adiciona arestas com capacidade 1 e custo igual ao peso
    for u in adj_list:
        for v in adj_list[u]:
            edge = f"{min(str(u), str(v))}-{max(str(u), str(v))}"  # Garantir que as chaves sejam strings
            weight = edge_weights.get(edge, None)  # Usando .get() para evitar KeyError
            if weight is not None:  # Só adiciona aresta se o peso existir
                G.add_edge(u, v, capacity=1, weight=weight)

    # Adiciona fonte e sumidouro
    source, sink = "s", "t"
    G.add_node(source)
    G.add_node(sink)

    for u in adj_list:
        G.add_edge(source, u, capacity=num_agents, weight=0)
        G.add_edge(u, sink, capacity=num_agents, weight=0)

    return G, source, sink


# Função para aplicar o algoritmo de Fleury
def fleury_algorithm(start, adj_list):
    graph = defaultdict(list, {u: list(v) for u, v in adj_list.items()})
    circuit = []

    def is_bridge(u, v):
        if len(graph[u]) == 1:
            return False
        visited = set()

        def dfs(node):
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(u)
        count1 = len(visited)
        graph[u].remove(v)
        graph[v].remove(u)
        visited.clear()
        dfs(u)
        count2 = len(visited)
        graph[u].append(v)
        graph[v].append(u)
        return count1 > count2

    def find_path(u):
        for v in list(graph[u]):
            if not is_bridge(u, v):
                graph[u].remove(v)
                graph[v].remove(u)
                find_path(v)
        circuit.append(u)

    find_path(start)
    return circuit


# Função principal para resolver o problema
def solve_mcpp(adjacency_list_file, edge_weights_file, start_node):
    # Carrega os arquivos
    adj_list, edge_weights = load_graph_files(adjacency_list_file, edge_weights_file)

    # Torna o grafo Euleriano
    added_edges = make_eulerian(adj_list, edge_weights)

    # Constrói o grafo de fluxo
    # flow_graph, source, sink = build_flow_graph(adj_list, edge_weights, num_agents)
    
    # Resolve o fluxo de custo mínimo
    # flow_dict = nx.min_cost_flow(flow_graph)
    # print("Fluxos calculados:", flow_dict)  # Adicionando print para depurar os fluxos


    # # Resolve o fluxo de custo mínimo
    # flow_dict = nx.min_cost_flow(flow_graph)

    # # Divide as arestas entre os agentes
    # agent_paths = defaultdict(list)
    # for u in flow_dict:
    #     for v, flow in flow_dict[u].items():
    #         if flow > 0 and u != "s" and v != "t":
    #             agent_paths[u].append(v)

    # # Aplica Fleury para encontrar os circuitos para cada agente
    # circuits = []
    # for start_node in agent_paths:
    #     if agent_paths[start_node]:
    #         circuit = fleury_algorithm(start_node, adj_list)
    #         circuits.append(circuit)

    # return circuits, added_edges
    
    return fleury_algorithm(start_node, adj_list)
    


# Configuração de arquivos e parâmetros
adjacency_list_file = "/home/joaoleaogf/joker/GrafosGrupo7-main/referencial/adjacency_list.json"
edge_weights_file = "/home/joaoleaogf/joker/GrafosGrupo7-main/referencial/arestas_pesos.json"
start_node = 61

# Solução
circuits = solve_mcpp(adjacency_list_file, edge_weights_file, start_node)
print("Circuitos:", circuits)

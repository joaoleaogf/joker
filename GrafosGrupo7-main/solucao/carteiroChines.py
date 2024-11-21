import json
import networkx as nx
from itertools import combinations
from collections import defaultdict
from networkx import MultiGraph

# # Caminhos para os arquivos 
# adjacency_list_file = "GrafosGrupo7-main/referencial/adjacency_list.json"
# edge_weights_file = "GrafosGrupo7-main/referencial/arestas_otimizadas.json"


# esq_adjacency_list_file = "GrafosGrupo7-main/esquinas/adjacency_list.json"
# esq_edge_weights_file = "GrafosGrupo7-main/esquinas/arestas_pesos_list.json"

# # Definir o vértice inicial fixo
# fixed_start_node = 61

def fleury_algorithm_circuit(graph: MultiGraph, start_node):
    temp_graph = graph.copy()  # Cria uma cópia do grafo
    circuit = [start_node]  # Lista para armazenar o circuito
    current_node = start_node  # Começa no nó inicial

    while temp_graph.number_of_edges() > 0:
        # Recupera os vizinhos do nó atual
        neighbors = list(temp_graph.neighbors(current_node))

        if not neighbors:
            raise ValueError(f"O nó {current_node} não possui vizinhos, mas ainda há arestas no grafo.")

        # Identificar uma aresta válida
        selected_neighbor = None
        for neighbor in neighbors:
            # Recuperar chaves das arestas entre o nó atual e o vizinho
            edge_keys = list(temp_graph[current_node][neighbor].keys())
            key = edge_keys[0]  # Seleciona a primeira chave disponível
            temp_graph.remove_edge(current_node, neighbor, key)  # Remove temporariamente

            # Verifica se a aresta é uma ponte
            if nx.has_path(temp_graph, current_node, neighbor):
                selected_neighbor = neighbor
                break
            else:
                # Reverte a remoção se a aresta for uma ponte
                temp_graph.add_edge(current_node, neighbor, key=key)

        # Caso todas as arestas sejam pontes, seleciona a primeira disponível
        if selected_neighbor is None:
            neighbor = neighbors[0]
            edge_keys = list(temp_graph[current_node][neighbor].keys())
            key = edge_keys[0]
            temp_graph.remove_edge(current_node, neighbor, key)
            selected_neighbor = neighbor

        # Atualiza o circuito e o nó atual
        circuit.append(selected_neighbor)
        current_node = selected_neighbor

    return circuit




def carteiroChines(adj_list, edge_weights_list, start_node):

    G = nx.MultiGraph()
    
    # Conjunto para rastrear arestas já adicionadas
    added_edges = set()

    for node, neighbors in adj_list.items():
        for neighbor in neighbors:
            # Criar uma representação ordenada da aresta para evitar duplicados
            edge_key = tuple(sorted([int(node), int(neighbor)]))
            
            # Verificar se a aresta já foi adicionada
            if edge_key in added_edges:
                continue
            
            # Buscar o peso da aresta, independentemente da ordem
            weight = edge_weights_list.get(f"{node}-{neighbor}") or edge_weights_list.get(f"{neighbor}-{node}") or 1
            
            # Adicionar aresta ao grafo e ao conjunto de rastreamento
            G.add_edge(edge_key[0], edge_key[1], weight=weight)
            added_edges.add(edge_key)


    # Verificar se o grafo é euleriano
    if nx.is_eulerian(G):
        print("O grafo já é euleriano.")

    else: 
        print("O grafo não é euleriano. Convertendo")
        
        print("Numero de arestas originais", nx.number_of_edges(G))
        print("Vértices com grau ímpar originais:", [node for node in G.nodes if G.degree[node] % 2 != 0])
        # Encontrar vértices de grau ímpar
        odd_degree_nodes = [node for node in G.nodes if G.degree[node] % 2 != 0]

        # Criar grafo completo (grafo Kn) entre os vértices de grau ímpar
        K = nx.Graph()
        for u, v in combinations(odd_degree_nodes, 2):
            shortest_path_length = nx.dijkstra_path_length(G, source=u, target=v, weight="weight")
            K.add_edge(u, v, weight=shortest_path_length)

        # Encontrar o emparelhamento perfeito mínimo no grafo Kn
        min_weight_matching = nx.algorithms.matching.min_weight_matching(K)

        # Adicionar as arestas do emparelhamento perfeito ao grafo original
        duplicated_edges = []  # Lista para rastrear arestas duplicadas
        for u, v in min_weight_matching:
            shortest_path = nx.dijkstra_path(G, source=u, target=v, weight="weight")
            
            for i in range(len(shortest_path) - 1):
                edge_key = f"{shortest_path[i]}-{shortest_path[i + 1]}"
                reversed_edge_key = f"{shortest_path[i + 1]}-{shortest_path[i]}"
                
                # Verificar se a aresta já existe
                duplicated_edges.append([shortest_path[i], shortest_path[i + 1]])
                
        # Adiciona duplicações ao grafo
        for u, v in duplicated_edges:
            edge_key = f"{u}-{v}"
            reversed_edge_key = f"{v}-{u}"
            weight = edge_weights_list.get(edge_key) or edge_weights_list.get(reversed_edge_key) or 1
            G.add_edge(int(u), int(v), weight=weight)

        print("Numero de arestas duplicadas", len(duplicated_edges))
        print("Euleriano (após revalidação):", nx.is_eulerian(G))
        
    print("Calculando circuito euleriano com fleury")
    result = fleury_algorithm_circuit(G, start_node)
    print("Circuito euleriano:", result)
    return result


# print("Executanto calculo pra solução na modelagem 'Quarteirões'")

# # Carregar lista de adjacência
# with open(adjacency_list_file, "r") as file:
#     adj_list = json.load(file)

# # Carregar pesos das arestas
# with open(edge_weights_file, "r") as file:
#     edge_weights_list = json.load(file)


# carteiroChines(adj_list, edge_weights_list, fixed_start_node)

# print("Executanto calculo pra solução na modelagem 'Esquinas'")

# # Carregar lista de adjacência
# with open(esq_adjacency_list_file, "r") as file:
#     adj_list = json.load(file)

# # Carregar pesos das arestas
# with open(esq_edge_weights_file, "r") as file:
#     edge_weights_list = json.load(file)


# carteiroChines(adj_list, edge_weights_list, fixed_start_node)
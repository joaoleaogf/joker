import json
import networkx as nx
from itertools import combinations

# Caminhos para os arquivos
adjacency_list_file = "/home/ddmx/Documentos/plataforma/joker/GrafosGrupo7-main/referencial/adjacency_list.json"
weights_file = "/home/ddmx/Documentos/plataforma/joker/GrafosGrupo7-main/referencial/distribuicao_quarteiroes.json"
edge_weights_file = "/home/ddmx/Documentos/plataforma/joker/GrafosGrupo7-main/referencial/arestas_otimizadas.json"
output_edges_file = "/home/ddmx/Documentos/plataforma/joker/GrafosGrupo7-main/referencial/arestas_otimizadas-2.json"
output_duplicated_edges = "/home/ddmx/Documentos/plataforma/joker/GrafosGrupo7-main/referencial/duplicated_edges.json"

# Carregar lista de adjacência
with open(adjacency_list_file, "r") as file:
    adj_list = json.load(file)

# Carregar pesos das arestas
with open(edge_weights_file, "r") as file:
    edge_weights_list = json.load(file)

# Converter a lista de pesos de arestas em um dicionário
edge_weights = {item["key"]: item["value"] for item in edge_weights_list}

# Criar grafo simples
G = nx.Graph()
for node, neighbors in adj_list.items():
    for neighbor in neighbors:
        edge_key = f"{node}-{neighbor}"
        reversed_edge_key = f"{neighbor}-{node}"
        
        # Buscar o peso da aresta, independentemente da ordem
        weight = edge_weights.get(edge_key) or edge_weights.get(reversed_edge_key) or 1
        G.add_edge(int(node), int(neighbor), weight=weight)

# Verificar se o grafo é euleriano
if nx.is_eulerian(G):
    print("O grafo já é euleriano.")
    with open(output_edges_file, "w") as file:
        json.dump(edge_weights_list, file)
    exit()

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
        if edge_key in edge_weights or reversed_edge_key in edge_weights:
            duplicated_edges.append([shortest_path[i], shortest_path[i + 1]])
        else:
            # Adicionar a nova aresta com peso padrão
            duplicated_edges.append([shortest_path[i], shortest_path[i + 1]])

# Salvar duplicações em um arquivo JSON
with open(output_duplicated_edges, "w") as file:
    json.dump(duplicated_edges, file)

# Atualizar a lista de pesos das arestas otimizadas
updated_edge_weights = edge_weights_list + [
    {"key": f"{u}-{v}", "value": G[u][v]["weight"]}
    for u, v in duplicated_edges
]

# Salvar arestas otimizadas no formato original
with open(output_edges_file, "w") as file:
    json.dump(updated_edge_weights, file)

# Printa as arestas duplicadas
print("Arestas duplicadas:")
for edge in duplicated_edges:
    print(edge)

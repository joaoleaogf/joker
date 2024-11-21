import heapq
from collections import defaultdict
import json
from carteiroChines import carteiroChines

# Função para processar o mapa de arestas e pesos
def process_edge_weight_map(edge_weight_map):
    adj_list = defaultdict(list)
    for edge, weight in edge_weight_map.items():
        vertex1, vertex2 = edge.split('-')
        vertex1, vertex2 = int(vertex1), int(vertex2)
        adj_list[vertex1].append((vertex2, weight))
        adj_list[vertex2].append((vertex1, weight))
    return adj_list

# Função para calcular a MST usando Dijkstra
def dijkstra_mst(adj_list, source):
    visited = set()
    mst = defaultdict(list)
    min_heap = [(0, source, None)]  # (peso, nó atual, nó pai)

    while min_heap:
        weight, current, parent = heapq.heappop(min_heap)
        if current in visited:
            continue
        visited.add(current)
        if parent is not None:
            mst[parent].append((current, weight))
            mst[current].append((parent, weight))
        for neighbor, edge_weight in adj_list[current]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_weight, neighbor, current))
    return mst

# Função para dividir a MST entre N agentes
def divide_mst_n_agents(mst, source, n_agents):
    subgraphs = [defaultdict(list) for _ in range(n_agents)]
    weights = [0] * n_agents  # Peso acumulado de cada subgrafo

    def dfs(node, parent):
        # Pilha auxiliar para explorar a MST
        stack = [(node, parent)]
        while stack:
            current, parent = stack.pop()
            for neighbor, weight in mst[current]:
                if neighbor == parent:
                    continue
                # Escolher o subgrafo com menor peso acumulado
                idx = weights.index(min(weights))
                subgraphs[idx][f"{current}-{neighbor}"] = weight
                subgraphs[idx][f"{neighbor}-{current}"] = weight
                weights[idx] += weight
                stack.append((neighbor, current))

    dfs(source, None)
    return subgraphs, weights

# Função para salvar os subgrafos em um arquivo no formato desejado
def save_agents_subgraphs(subgraphs, weights, filename="agents_subgraphs.json"):
    agents_data = []
    
    for i, subgraph in enumerate(subgraphs):
        agent_data = {
            **subgraph
        }
        agents_data.append(agent_data)
    
    # Salvar no formato JSON
    with open(filename, "w") as file:
        json.dump(agents_data, file, indent=4)


def carteiroChinesMulti(adj_list, edge_weights_list, start_node, agentes):
    print(f"\033[1m Realizando Cálculo divisão da MST entre os Agentes \033[0m \n")
    
    # Passo 1: Processar o mapa de arestas e pesos para criar o grafo
    adj_list_2 = process_edge_weight_map(edge_weights_list)

    # Passo 2: Construir a MST usando Dijkstra (a partir do start_node)
    mst = dijkstra_mst(adj_list_2, start_node)

    # Passo 3: Dividir a MST entre N agentes
    subgraphs, weights = divide_mst_n_agents(mst, start_node, agentes)        
    
    for idx, subgraph in enumerate(subgraphs):
        print(f"\033[1m Agente {idx + 1} \033[0m")
    
        carteiroChines(adj_list, subgraph, start_node)
        print(" \n \n")


# Caminhos para os arquivos 
adjacency_list_file = "GrafosGrupo7-main/referencial/adjacency_list.json"
edge_weights_file = "GrafosGrupo7-main/referencial/arestas_pesos.json"


esq_adjacency_list_file = "GrafosGrupo7-main/esquinas/adjacency_list.json"
esq_edge_weights_file = "GrafosGrupo7-main/esquinas/arestas_pesos.json"

   


print(f"\033[1m Executanto calculo pra solução na modelagem 'Quarteirões' \033[0m \n")

with open(adjacency_list_file, "r") as file:
    adj_list = json.load(file)
    
with open(edge_weights_file, "r") as file:
    edge_weights_list = json.load(file)
    
carteiroChinesMulti(adj_list, edge_weights_list, 61, 3)

print(f"\033[1m Executanto calculo pra solução na modelagem 'Esquinas' \033[0m \n")

with open(esq_adjacency_list_file, "r") as file:
    esq_adj_list = json.load(file)
    
with open(esq_edge_weights_file, "r") as file:
    esq_weights = json.load(file)

carteiroChinesMulti(esq_adj_list, esq_weights, 54, 3)

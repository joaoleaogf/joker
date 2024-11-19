import json

# Caminho para o arquivo adjacency_list.json
adjacency_list_file = "/home/joaoleaogf/joker/GrafosGrupo7-main/referencial/adjacency_list.json"
input_edges_file = "/home/joaoleaogf/joker/GrafosGrupo7-main/referencial/arestas_otimizadas.json"
output_weights_file = "/home/joaoleaogf/joker/GrafosGrupo7-main/esquinas/arestas_pesos.json"
output_adjacency_list_file = "/home/joaoleaogf/joker/GrafosGrupo7-main/esquinas/adjacency_list.json"

def encontrar_areas_unicas(adjacency_list):
    # Conjuntos para garantir unicidade
    triangulos_unicos = set()
    quadrilateros_unicos = set()

    # Percorrer cada vértice
    for v in adjacency_list:
        adj_v = adjacency_list[v]  # Vizinhos de v
        
        # **Encontrar Triângulos**
        for u in adj_v:
            for w in adj_v:
                if u >= w:  # Evitar duplicação e garantir u < w
                    continue
                if w in adjacency_list[u]:  # Triângulo: u-v-w
                    triangulo = tuple(sorted([v, u, w]))
                    triangulos_unicos.add(triangulo)

        # **Encontrar Quadriláteros**
        for u in adj_v:
            for w in adj_v:
                if u >= w:  # Evitar duplicação e garantir u < w
                    continue
                
                # Verificar se u e w compartilham um adjacente
                comuns = set(adjacency_list[u]).intersection(adjacency_list[w])
                for x in comuns:
                    if x != v:  # Evitar ciclos triviais
                        quadrilatero = tuple(sorted([v, u, w, x]))
                        quadrilateros_unicos.add(quadrilatero)

    # Combinar os dois conjuntos em uma lista única, ordenada
    areas_unicas = sorted(list(triangulos_unicos) + list(quadrilateros_unicos))
    
    return areas_unicas


# Ler a lista de adjacência do arquivo
with open(adjacency_list_file, "r") as file:
    adjacency_list = json.load(file)

# **Converter as chaves para inteiros (se necessário)**
adjacency_list = {int(k): v for k, v in adjacency_list.items()}

# Chamar a função para encontrar áreas únicas
areas = encontrar_areas_unicas(adjacency_list)

def criar_lista_adjacencia_areas(areas, arestas):

    # Criar uma lista de adjacência baseada em áreas
    adjacencia_areas = {i: set() for i in range(len(areas))}
    pesos = {}

    # Processar arestas e verificar relações entre áreas
    for aresta in arestas:
        v1, v2 = map(int, aresta["key"].split("-"))
        
        esquinas = []
        
        for idx, area in enumerate(areas):
            if v1 in area and v2 in area:
                esquinas.append(idx)
        
        if len(esquinas) < 2:
            continue
        
        area1 = esquinas[0]
        area2 = esquinas[1]
        
        adjacencia_areas[area1].add(area2)
        adjacencia_areas[area2].add(area1)
        pesos[f"{area1}-{area2}"] = aresta["value"]
                       

    # Converter sets em listas para uma lista de adjacência padrão
    adjacencia_areas = {k: list(v) for k, v in adjacencia_areas.items()}
    return adjacencia_areas, pesos

# Ler a lista de áreas (adjacency_list.json)
with open(adjacency_list_file, "r") as file:
    adjacency_list = json.load(file)

# Converter as chaves para inteiros (caso necessário)
adjacency_list = {int(k): v for k, v in adjacency_list.items()}

# Ler a lista de arestas (arestas_otimizadas.json)
with open(input_edges_file, "r") as file:
    edges = json.load(file)

# Criar a nova lista de adjacência baseada nas áreas
nova_lista_adjacencia, pesos = criar_lista_adjacencia_areas(areas, edges)

with open(output_weights_file, "w") as file:
    json.dump(pesos, file, indent=4)

with open(output_adjacency_list_file, "w") as file:
    json.dump(nova_lista_adjacencia, file, indent=4)

# Exibir a nova lista de adjacência
print("Nova lista de adjacência baseada em Esquinas feita")
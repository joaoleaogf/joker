import json
from igraph import Graph, plot

# Caminho para o arquivo de arestas otimizadas
input_edges_file = "/home/joaoleaogf/joker/GrafosGrupo7-main/esquinas/arestas_pesos.json"
output_graph_file = "/home/joaoleaogf/joker/GrafosGrupo7-main/esquinas/grafo_arestas_otimizadas.png"

# Carregar as arestas otimizadas do arquivo JSON
with open(input_edges_file, "r") as file:
    edges_data = json.load(file)

# Construir as arestas e pesos a partir dos dados
edges = set()  # Usar um set para garantir unicidade das arestas
weights = []

for key, weight in edges_data.items():
    u, v = map(int, key.split("-"))  # Extrair os vértices da chave "u-v"
    
    # Adicionar a aresta sem duplicação (u, v) ou (v, u) é a mesma
    if u != v:  # Evitar laços (auto-conexões)
        edges.add(tuple(sorted((u, v))))  # Usar sorted para garantir que (u, v) e (v, u) sejam tratados como a mesma aresta
        weights.append(weight)

# Criar o grafo
g = Graph(directed=False)
g.add_vertices(max(max(u, v) for u, v in edges) + 1)  # Adicionar todos os vértices necessários
g.add_edges(list(edges))  # Adicionar as arestas únicas

# Adicionar pesos das arestas
g.es["weight"] = weights
g.es["label"] = [f"{peso:.2f}" for peso in weights]

# Configurar estilos de visualização
visual_style = {
    "vertex_label": [str(i) for i in range(len(g.vs))],
    "vertex_color": "white",  # Vértices sem cor (brancos)
    "vertex_frame_color": "black",  # Borda dos vértices em preto
    "edge_label": g.es["label"],  # Rótulos com os pesos das arestas
    "bbox": (800, 800),
    "margin": 50,
}

# Renderizar o grafo e salvar a imagem
plot(g, **visual_style)
plot(g, output_graph_file, **visual_style)

# Exibir informações finais
print(f"Número de vértices: {len(g.vs)}")
print(f"Número de arestas: {len(g.es)}")
print(f"Grafo salvo como '{output_graph_file}'")

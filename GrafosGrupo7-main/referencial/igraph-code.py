import json
from igraph import Graph, plot

# Carregar a lista de adjacência do arquivo JSON
with open("/home/joaoleaogf/documents/logs/GrafosGrupo7-main/referencial/adjacency_list.json", "r") as file:
    adj_list = json.load(file)

# Criar as arestas a partir da lista de adjacência
edges = []
weights = []

for source, targets in adj_list.items():
    for target, weight in targets:
        edges.append((int(source), int(target)))
        weights.append(weight)

# Criar o grafo
g = Graph(edges=edges, directed=False)

# Adicionar pesos como atributo de aresta
g.es["weight"] = weights

# Configurar estilos de visualização
visual_style = {
    "vertex_label": [str(i) for i in range(len(g.vs))],
    "vertex_color": "white",  # Vértices sem cor (brancos)
    "vertex_frame_color": "black",  # Borda dos vértices em preto
    "edge_width": [weight / max(weights) * 5 for weight in weights],
    "edge_label": weights,  # Exibir os pesos das arestas como rótulos
    "bbox": (800, 800),
    "margin": 50,
}

# Renderizar o grafo
plot(g, **visual_style)
plot(g, "/home/joaoleaogf/documents/logs/GrafosGrupo7-main/referencial/grafo2.png", **visual_style)
print("Grafo salvo como 'grafo3.png'")

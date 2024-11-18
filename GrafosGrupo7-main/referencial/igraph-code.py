import json
from igraph import Graph, plot

# Carregar a lista de adjacência do arquivo JSON
with open("/home/joaoleaogf/documents/logs/GrafosGrupo7-main/referencial/adjacency_list.json", "r") as file:
    adj_list = json.load(file)

# Criar as arestas a partir da lista de adjacência
edges = []

for source, targets in adj_list.items():
    for target in targets:
        edges.append((int(source), int(target)))

# Criar o grafo
g = Graph(edges=edges, directed=False)

# Configurar estilos de visualização
visual_style = {
    "vertex_label": [str(i) for i in range(len(g.vs))],
    "vertex_color": "white",  # Vértices sem cor (brancos)
    "vertex_frame_color": "black",  # Borda dos vértices em preto
    "bbox": (800, 800),
    "margin": 50,
}

# Renderizar o grafo
plot(g, **visual_style)
plot(g, "/home/joaoleaogf/documents/logs/GrafosGrupo7-main/referencial/grafo2.png", **visual_style)
print("Grafo salvo como 'grafo3.png'")

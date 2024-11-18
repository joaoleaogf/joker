import json
from igraph import Graph, plot

# Caminho para o arquivo de arestas otimizadas
input_edges_file = "/home/ddmx/Documentos/plataforma/joker/GrafosGrupo7-main/referencial/arestas_otimizadas-2.json"
output_graph_file = "/home/ddmx/Documentos/plataforma/joker/GrafosGrupo7-main/referencial/grafo_arestas_otimizadas.png"

# Carregar as arestas otimizadas do arquivo JSON
with open(input_edges_file, "r") as file:
    edges_data = json.load(file)

# Construir as arestas e pesos a partir dos dados
edges = [(int(key.split("-")[0]), int(key.split("-")[1])) for key in [item["key"] for item in edges_data]]
weights = [item["value"] for item in edges_data]

# Criar o grafo multiarestas
g = Graph(directed=False)
g.add_vertices(max(max(u, v) for u, v in edges) + 1)  # Adicionar todos os vértices necessários
g.add_edges(edges)

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

# Renderizar o grafo
plot(g, **visual_style)
plot(g, output_graph_file, **visual_style)

# Exibir informações finais
print(f"Número de vértices: {len(g.vs)}")
print(f"Número de arestas: {len(g.es)}")
print(f"Grafo salvo como '{output_graph_file}'")

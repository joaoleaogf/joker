import json
from igraph import Graph, plot

# Caminhos para os arquivos
adjacency_list_file = "/home/ddmx/Documentos/plataforma/joker/GrafosGrupo7-main/referencial/adjacency_list.json"
weights_file = "/home/ddmx/Documentos/plataforma/joker/GrafosGrupo7-main/referencial/distribuicao_quarteiroes.json"
output_graph_file = "/home/ddmx/Documentos/plataforma/joker/GrafosGrupo7-main/referencial/grafo_pesos.png"
output_weights_file = "/home/ddmx/Documentos/plataforma/joker/GrafosGrupo7-main/referencial/arestas_pesos.json"

# Carregar a lista de adjacência do arquivo JSON
with open(adjacency_list_file, "r") as file:
    adj_list = json.load(file)

# Carregar os pesos dos quarteirões
with open(weights_file, "r") as file:
    quarteirao_pesos = json.load(file)

# Criar as arestas únicas a partir da lista de adjacência
edges = set()
for source, targets in adj_list.items():
    for target in targets:
        edge = tuple(sorted((int(source), int(target))))
        edges.add(edge)

# Criar o grafo
g = Graph(edges=list(edges), directed=False)

# Contar arestas incidentes em cada vértice
grau_vertices = g.degree()

# Calcular pesos das arestas
arestas_pesos = {}
for edge in edges:
    source, target = edge
    peso_source = quarteirao_pesos[str(source)] / grau_vertices[source]
    peso_target = quarteirao_pesos[str(target)] / grau_vertices[target]
    peso_aresta = (peso_source + peso_target) / 2  # Média dos pesos incidentes
    arestas_pesos[edge] = peso_aresta

# Transformar chaves do dicionário de tuplas para strings
arestas_pesos_str = {f"{edge[0]}-{edge[1]}": peso for edge, peso in arestas_pesos.items()}

# Salvar os pesos das arestas em um arquivo JSON
with open(output_weights_file, "w") as file:
    json.dump(arestas_pesos_str, file, indent=4)

# Adicionar pesos das arestas como rótulos no grafo
g.es["label"] = [f"{arestas_pesos[tuple(sorted(edge))]:.2f}" for edge in g.get_edgelist()]

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
print(f"Pesos das arestas salvos como '{output_weights_file}'")

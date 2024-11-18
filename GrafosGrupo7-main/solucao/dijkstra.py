class Graph:
    def __init__(self, vertices):
        self.V = vertices  # quantidade de vertices
        self.graph = []  # guarda as arestas com vertices que relacionam ela e os pesos, exemplo 0 até 1 com peso 4

    # como o grafo não é direcionado faz o "vai e volta", recebe vertice inicial, final e peso
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])
        self.graph.append([v, u, w])

    def minDistance(self, dist, T):  # recebo os parametros
        min = float('inf')  # marcado com inf
        for v in range(self.V):  # itero sobre ele
            # se a dist na posição v for menor que min(infinito) e o vetor t na posicao v for falso
            if dist[v] < min and T[v] == False:
                # min recebe o valor da dist na posição v, porque ele quer o menor caminho
                min = dist[v]
                min_index = v  # vetor min_index(resultado) recebe o vertice v
        return min_index  # retorna

    def printSolution(self, dist):
        print("Vértice da Origem")
        for node in range(self.V):
            print(node, "\t", dist[node])

    def dijsktra(self, src):  # começa aqui, recebe o vertice inicial
        dist = [float('inf')] * self.V  # vetor dist seta todos com infinito
        dist[src] = 0  # distancia do primeiro vertice para ele mesmo é zero
        T = [False] * self.V  # vetor t marcado tudo como falso, não está visitado
        for count in range(self.V):  # entro no for iterando em todos os vértices
            # chamo a funcao de distancia minima para o vetor dist e o t
            u = self.minDistance(dist, T)
            for v in range(self.V):
                for item in self.graph:
                    if (item[0] == u) and (item[1] == v):
                        if item[2] > 0 and T[v] == False and dist[v] > dist[u]+item[2]:
                            dist[v] = dist[u]+item[2]
            T[u] = True
        self.printSolution(dist)

import cv2
import numpy as np
from scipy.spatial import distance
from collections import defaultdict

# Carregar a imagem
image = cv2.imread('/home/joaoleaogf/documents/logs/GrafosGrupo7-main/cena.jpg')

# Converter para escala de cinza e aplicar blur
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Aplicar detecção de bordas Canny
edges = cv2.Canny(blur, 50, 150)

# Encontrar contornos
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Filtrar contornos pequenos para ignorar ruído
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 800]

# Organizar contornos em grupos de quarteirões
# block_contours = []
# visited = set()

# def is_near(cnt1, cnt2, threshold=50):
#     """Verifica se dois contornos estão próximos usando distância mínima entre eles."""
#     for p1 in cnt1:
#         for p2 in cnt2:
#             if distance.euclidean(p1[0], p2[0]) < threshold:
#                 return True
#     return False

# for i, cnt1 in enumerate(filtered_contours):
#     if i in visited:
#         continue
#     block = [cnt1]
#     visited.add(i)
#     for j, cnt2 in enumerate(filtered_contours):
#         if j not in visited and is_near(cnt1, cnt2):
#             block.append(cnt2)
#             visited.add(j)
#     block_contours.append(block)

# # Contar lotes por quarteirão e criar o mapa de pesos
# block_weights = {}
# for idx, block in enumerate(block_contours):
#     block_weights[idx] = len(block)  # número de lotes no quarteirão

# # Criar a matriz de adjacência
# num_blocks = len(block_contours)
# adj_matrix = np.zeros((num_blocks, num_blocks), dtype=int)

# for i in range(num_blocks):
#     for j in range(i + 1, num_blocks):
#         if any(is_near(cnt1, cnt2) for cnt1 in block_contours[i] for cnt2 in block_contours[j]):
#             adj_matrix[i, j] = adj_matrix[j, i] = 1  # Marcar como adjacentes

# # Exibir os resultados
# print("Mapa de pesos dos quarteirões (vértices):", block_weights)
# print("Matriz de adjacência dos quarteirões:")
# print(adj_matrix)

# # Opcional: Salvar imagem com contornos desenhados
image_with_contours = image.copy()
cv2.drawContours(image_with_contours, filtered_contours, -1, (0, 255, 0), 2)
cv2.imwrite('/home/joaoleaogf/documents/logs/GrafosGrupo7-main/resultado_quarteiroes_lotes_2.jpg', image_with_contours)

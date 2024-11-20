import cv2
import numpy as np

# Carregar a imagem
image = cv2.imread('/home/joaoleaogf/documents/logs/GrafosGrupo7-main/cena.jpg')

# Converter para escala de cinza
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar um blur para reduzir o ruído
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Aplicar a detecção de bordas Canny
edges = cv2.Canny(blur, 50, 150)

# Encontrar contornos na imagem
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Filtrar os contornos por tamanho (para eliminar ruído e detalhes pequenos)
filtered_contours = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 800:  # Define um limite de área mínima
        filtered_contours.append(cnt)

# Desenhar os contornos filtrados na imagem original
image_with_contours = image.copy()
cv2.drawContours(image_with_contours, filtered_contours, -1, (0, 255, 0), 2)

# Exibir a imagem com os contornos
# cv2.imshow('Quarteirões e Lotes Detectados', image_with_contours)

# Contar e imprimir o número de lotes identificados
num_lotes = len(filtered_contours)
print(f"Número de lotes identificados: {num_lotes}")

cv2.waitKey(0)
cv2.destroyAllWindows()

# Salvar a imagem processada
cv2.imwrite('/home/joaoleaogf/documents/logs/GrafosGrupo7-main/resultado_quarteiroes_lotes.jpg', image_with_contours)
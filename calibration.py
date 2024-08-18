import cv2 
import numpy as np 
import os 
import glob 

# Dimensões do checkerboard
CHECKERBOARD = (7,5) 

# Critérios de término para o algoritmo de refinamento de cantos
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) 

# Vetores para pontos 3D (no espaço real) e pontos 2D (no plano da imagem)
threedpoints = [] 
twodpoints = [] 

# Preparando os pontos 3D no espaço real, considerando um tabuleiro plano com (6, 9) cantos
objectp3d = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32) 
objectp3d[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2) 

# Carregando as imagens para calibração
images = glob.glob('images/*.png') 

# Verificação se imagens foram encontradas
if not images:
    print("Nenhuma imagem .png encontrada no diretório atual.")
    exit()

for filename in images: 
    image = cv2.imread(filename)
    
    if image is None:
        print(f"Erro ao carregar a imagem {filename}.")
        continue
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    # Encontrando os cantos do tabuleiro de xadrez
    ret, corners = cv2.findChessboardCorners(
        gray, CHECKERBOARD, 
        cv2.CALIB_CB_ADAPTIVE_THRESH + 
        cv2.CALIB_CB_FAST_CHECK +
        cv2.CALIB_CB_NORMALIZE_IMAGE
    ) 

    # Refinamento dos cantos e adição dos pontos 3D e 2D
    if ret:
        threedpoints.append(objectp3d) 
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria) 
        twodpoints.append(corners2) 
        image = cv2.drawChessboardCorners(image, CHECKERBOARD, corners2, ret) 
        cv2.imshow('img', image) 
        cv2.waitKey(500)  # Mostrar a imagem por 500ms
    else:
        print(f"Não foi possível encontrar o tabuleiro de xadrez na imagem {filename}.")

cv2.destroyAllWindows() 

if not threedpoints or not twodpoints:
    print("Não foi possível encontrar os pontos necessários para calibração.")
    exit()

# Realizando a calibração da câmera
ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(threedpoints, twodpoints, gray.shape[::-1], None, None) 

# Exibindo a saída requerida
print("Matriz da Câmera:") 
print(matrix) 

print("\nCoeficientes de Distorção:") 
print(distortion) 

print("\nVetores de Rotação:") 
print(r_vecs) 

print("\nVetores de Translação:") 
print(t_vecs) 

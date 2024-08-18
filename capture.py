import cv2
import keyboard
import time
import os

url = "http://192.168.0.150:8080/video"

cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Erro ao conectar à câmera.")
    exit()

save_dir = "images"

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

img_count = 0
img_list = []

print("Pressione a tecla 's' para capturar uma imagem. Pressione 'q' para sair.")

while img_count < 20:
    ret, frame = cap.read()
    
    if not ret:
        print("Erro ao receber frame da câmera.")
        break

    cv2.imshow("Camera", frame)

    if keyboard.is_pressed('s'):
        img_name = f"imagem_{img_count+1}.png"
        img_path = os.path.join(save_dir, img_name)
        img_list.append(frame)
        cv2.imwrite(img_path, frame)
        print(f"Imagem {img_name} capturada e salva em {save_dir}.")
        img_count += 1
        time.sleep(1)

    if keyboard.is_pressed('q'):
        print("Encerrando...")
        break

    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()

print("Processo concluído.")

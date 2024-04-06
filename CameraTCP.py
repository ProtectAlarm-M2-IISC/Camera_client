import cv2
import socket
import struct
import threading

# Définition de l'adresse IP et du port du serveur pccloud
server_ip = '195.45.29.02'  # mettre l'adresse IP du serveur pccloud
server_port = 23456  # mettre le port du pccloud

# Fonction pour envoyer le flux vidéo
def send_video():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    cap = cv2.VideoCapture(0)  # Utilisez 0 pour la webcam intégrée, ou l'index de la caméra souhaitée
    #cap.set(3, 320)  # Réduction de la largeur de l'image
    #cap.set(4, 240)  # Réduction de la hauteur de l'image
    cap.set(3, 160)  # Réduction supplémentaire de la largeur de l'image
    cap.set(4, 120)  # Réduction supplémentaire de la hauteur de l'image


    try:
        while True:
            ret, frame = cap.read()
            encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()

            # Envoyer la taille des données d'image
            client_socket.sendall(struct.pack('!I', len(encoded_frame)))

            # Envoyer les données d'image encodées
            client_socket.sendall(encoded_frame)
    finally:
        cap.release()
        client_socket.close()

# Démarrer le thread pour envoyer le flux vidéo
video_thread = threading.Thread(target=send_video)
video_thread.daemon = True
video_thread.start()

# Attendre que le thread se termine
video_thread.join()


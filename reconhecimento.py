# -*- coding: utf-8 -*-
<<<<<<< HEAD
import multiprocessing
from multiprocessing import Pipe
=======
import multiprocessing 
from multiprocessing import Pipe,Process    
>>>>>>> 68d5a46f2c59af66c7bbf2d522c95e45bdda6b90
import multiprocessing.dummy as mp
import face_recognition
import cv2
import time
import os
import Queue

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Referencia para a webcam #0 (default)
video_capture = cv2.VideoCapture(0)

# Carrega uma figura e aprende a reconhecer seus padroes.
leleo_image = face_recognition.load_image_file("leleo.jpg")
leleo_face_encoding = face_recognition.face_encodings(leleo_image)[0]

# Carrega uma segunda figura e aprende a reconhecer seus padroes.
bastos_image = face_recognition.load_image_file("bastos.jpg")
bastos_face_encoding = face_recognition.face_encodings(bastos_image)[0]

# Cria um array de faces conhecidas e seus nomes.
known_face_encodings = [
    leleo_face_encoding,
    bastos_face_encoding
]
known_face_names = [
    "Leleo",
    "Gabriel Bastos"
]

# Inicializa algumas variaveis

#rgb_small_frame

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
tempo_anterior = 0
tempo = 0
rgb_small_frame = Pipe(duplex=True)


#################
# Funcao para usar o multiprocessing do python

def face_match(face_encoding):
    # Ver se a face encontrada está entre as conhecidas
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Desconhecido"

        # Se der um "match" entre a face reconhecida e uma já conhecida, usa a primeira.
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    face_names.append(name)

# Funcao para capturar a imagem

<<<<<<< HEAD
def processar_video(rgb_small_frame):
    global face_match
    global face_encodings
=======

def capture_and_resize(ret,frame,rgb_small_frame):
    
    #global ret 
    #global frame
    #global rgb_small_frame

    ret, frame = video_capture.read() # Captura um frame do video
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # Redimensiona a imagem para 1/4 da qualidade original para melhorar o tempo de reconhecimento.
    rgb_small_frame = small_frame[:, :, ::-1] # Converte do padrao BRG (openCV usa) para o RGB (face_recognition usa).

#

def processar_video(face_names,face_locations):
    #global face_names
    #global face_locations
>>>>>>> 68d5a46f2c59af66c7bbf2d522c95e45bdda6b90

    if __name__ == '__main__':
    	pool = mp.Pool(2)
    	pool.map(face_match, face_encodings)
    	pool.close()
    	pool.join()

#################


while True:
    antes = time.time()
    processos = []
<<<<<<< HEAD
    face_names = []
    #frame = Pipe(duplex=False)

=======
    
>>>>>>> 68d5a46f2c59af66c7bbf2d522c95e45bdda6b90
    # Captura um frame do video
    #ret, frame = video_capture.read()

    # Redimensiona a imagem para 1/4 da qualidade original para melhorar o tempo de reconhecimento.
    #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Converte do padrao BRG (openCV usa) para RGB (face_recognition usa).
    #rgb_small_frame = small_frame[:, :, ::-1]
    
    #capture_and_resize()
<<<<<<< HEAD
    
    
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # Redimensiona a imagem para 1/4 da qualidade original para melhorar o tempo de reconhecimento.
    rgb_small_frame = small_frame[:, :, ::-1] # Converte do padrao BRG (openCV usa) para o RGB (face_recognition usa).
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
=======

    parent_frame,frame = Pipe()
    parent_ret,ret = Pipe()
    parent_rgb_small_frame,rgb_small_frame = Pipe()
    
    p1 = multiprocessing.Process(target=capture_and_resize,args=(ret,frame,rgb_small_frame))
    processos.append(p1)
    p1.start()
>>>>>>> 68d5a46f2c59af66c7bbf2d522c95e45bdda6b90
    # So processa um frame por vez para economizar tempo
    
    print(parent_frame)
    p1.join()

    if process_this_frame:

<<<<<<< HEAD
        p1 = multiprocessing.Process(target=processar_video, args=(rgb_small_frame,))
        processos.append(p1)
        p1.start()
=======
        print("processando")
        #processar_video()
        
        parent_face_names, face_names = Pipe()
        parent_face_locations, face_locations = Pipe()
    
        p2 = multiprocessing.Process(target=processar_video, args=(face_names,face_locations))
        processos.append(p2)
        p2.start()
>>>>>>> 68d5a46f2c59af66c7bbf2d522c95e45bdda6b90
        #process()
        # Procura todas as faces no video
        #face_locations = face_recognition.face_locations(rgb_small_frame)
        #face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        #face_names = []
        #if __name__ == '__main__':
	#	pool = mp.Pool(2)
	#	pool.map(face_match, face_encodings)
	#	pool.close()
	#	pool.join()

    process_this_frame = not process_this_frame


    # Mostra os resultados
    for (top, right, bottom, left), name in zip(parent_face_locations, parent_face_names):
        # Desfaz o tratamento 1/4 que fizemos no inicio
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        
        if (name=="Desconhecido"):
            # Desenha uma caixa em torno da pessoa
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Escreve o nome embaixo da caixa
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        else:
            # Desenha uma caixa em torno da pessoa
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Escreve o nome embaixo da caixa
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
    # Mostra a imagem resultante
    p1.join()
    cv2.imshow('Video', frame)
        #p2 = multiprocessing.Process(target=cv2.imshow, args=('Video', frame,))
        #processos.append(p2)
        #p2.start()

    agora = time.time()
    diferenca = (agora - antes)
    print (diferenca)

    #p1.join()

    # Aperte 'q' para sair!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fecha a conexao com a webcam

#p2.join()
agora = time.time()
diferenca = (agora - antes)
print (diferenca)
video_capture.release()
cv2.destroyAllWindows()

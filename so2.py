# -*- coding: utf-8 -*-
import multiprocessing.dummy as mp
import face_recognition
import cv2
import time
########################################
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from setupbd import Base, All_people, Pessoa, Usuario

engine = create_engine("mysql+mysqldb://root:password@localhost/so2018")
#engine = create_engine('mysql+mysqldb://so2018:bastoseleleo123@so2018.mysql.pythonanywhere-services.com/so2018$default')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


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

rodrigo_image = face_recognition.load_image_file("rodrigo.png")
rodrigo_face_encoding = face_recognition.face_encodings(rodrigo_image)[0]

fabiana_image = face_recognition.load_image_file("fabiana.jpg")
fabiana_face_encoding = face_recognition.face_encodings(fabiana_image)[0]

ronaldo_image = face_recognition.load_image_file("ronaldo.jpg")
ronaldo_face_encoding = face_recognition.face_encodings(ronaldo_image)[0]

japones_image = face_recognition.load_image_file("japones.jpg")
japones_face_encoding = face_recognition.face_encodings(japones_image)[0]

estranho_image = face_recognition.load_image_file("estranho.jpg")
estranho_face_encoding = face_recognition.face_encodings(estranho_image)[0]


# Cria um array de faces conhecidas e seus nomes.
global face_names
global known_face_encodings

known_face_encodings = [
    leleo_face_encoding,
    bastos_face_encoding,
    rodrigo_face_encoding,
    fabiana_face_encoding,
    ronaldo_face_encoding,
    japones_face_encoding,
    estranho_face_encoding
]

known_face_names = [
    "Leonardo Feliciano",
    "Gabriel Bastos",
    "Rodrigo Couto",
    "Fabiana Ferreira",
    "Ronaldo",
    "Japones",
    "Estranho"

]

# Inicializa algumas variaveis
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
tempo_anterior = 0
tempo = 0

dataAtual = datetime.now().strftime('%d/%m/%Y')

#################
# Funcao para usar o multiprocessing do python

def face_match(face_encoding):

    # Ver se a face encontrada esta entre as conhecidas
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Desconhecido"

        # Se der um "match" entre a face reconhecida e uma já conhecida, usa a primeira.
    if True in matches:

        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    face_names.append(name)

# Funcao para capturar a imagem

def capture_and_resize():
    
    global frame
    global ret
    global rgb_small_frame
    ret, frame = video_capture.read() # Captura um frame do video
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) # Redimensiona a imagem para 1/4 da qualidade original para melhorar o tempo de reconhecimento.
    rgb_small_frame = small_frame[:, :, ::-1] # Converte do padrao BRG (openCV usa) para o RGB (face_recognition usa).

#################

while True:
    antes = time.time()

    capture_and_resize()

    '''
    # Captura um frame do video
    ret, frame = video_capture.read()

    # Redimensiona a imagem para 1/4 da qualidade original para melhorar o tempo de reconhecimento.
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Converte do padrao BRG (openCV usa) para RGB (face_recognition usa).
    rgb_small_frame = small_frame[:, :, ::-1]
    '''
    # So processa um frame por vez para economizar tempo
    if process_this_frame:
        # Procura todas as faces no video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        if __name__ == '__main__':

            pool = mp.Pool(1)
            pool.map(face_match, face_encodings)
            pool.close()
            pool.join()

    process_this_frame = not process_this_frame


    # Mostra os resultados
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Desfaz o tratamento 1/4 que fizemos no inicio
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4


        if (name == "Desconhecido"):
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
        
        if (name != "Desconhecido"):

            people = session.query(All_people).filter_by(name=name).one()
            pessoas = session.query(Pessoa).filter_by(nome=name).all()

            for pessoa in pessoas:
                print ("Conectando ao Banco....")

            if (pessoa.data != dataAtual):

                insert = Pessoa(nome=name, dre = people.dre, data=dataAtual, hora_chegada=datetime.now().strftime('%H:%M:%S'), hora_saida=pessoa.hora_saida)
                session.add(insert)
                session.commit()
            else:
                session.query(Pessoa).filter_by(nome=name).filter_by(data=dataAtual).update({"hora_saida": datetime.now().strftime('%H:%M:%S')})
                session.commit()


    # Mostra a imagem resultante
    cv2.imshow('Video', frame)

    agora = time.time()
    diferenca = (agora - antes)
    print ("Diferenca:",diferenca)

    # Aperte 'q' para sair!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fecha a conexao com a webcam
agora = time.time()
diferenca = (agora - antes)
print (diferenca)
video_capture.release()
cv2.destroyAllWindows()


from config import *
from cv2 import cv2
import face_recognition as fr
import numpy
from datetime import datetime
from base.models import Asistencia

print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

ruta = 'Estudiantes'
mis_imagenes = []
nombres_estudiantes = []
lista_rutas_estudiantes = os.listdir(ruta)
for estudiante in lista_rutas_estudiantes:
    imagen_cargada = cv2.imread(f'{ruta}/{estudiante}')
    mis_imagenes.append(imagen_cargada)
    nombres_estudiantes.append(os.path.splitext(estudiante)[0])


# codificar imagenes
def codificar(imagenes):
    lista_codificadas = []
    for img in imagenes:
        # convertir a rgb
        imagen = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # imagen codificada
        img_codif = fr.face_encodings(imagen)[0]

        lista_codificadas.append(img_codif)

    return lista_codificadas


# Registrar en csv
'''def registrar(persona):
    archivo = open('asistencia.csv', 'r+')
    registros = archivo.readlines()
    nombres_asistidos = []

    for linea in registros:
        nombres_asistidos.append(linea.split(',')[0])

    if persona not in nombres_asistidos:
        actual = datetime.now()
        str_actual = actual.strftime('%H:%M:%S')
        archivo.write(f'\n{persona}, {str_actual}')'''


# Registrar en DB
def registrar(persona):
    registros = Asistencia.objects.filter(nombre=persona)

    if not registros.exists():
        # Si no existe, crear un nuevo registro
        actual = datetime.now()
        nueva_asistencia = Asistencia(
            nombre=persona,
            fecha=actual.date(),
            hora=actual.time()
        )
        nueva_asistencia.save()  # Guarda el registro en la base de datos


estudiantes_Codificados = codificar(mis_imagenes)

url = "http://192.168.1.4:8080/video"

capturador = cv2.VideoCapture(url)

frame_count = 0
face_locations = []
face_encodings = []

while True:
    exito, frame = capturador.read()
    if not exito:
        print("Captura no tomada")
        break
    else:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # cada 15 frame se va localizar los rostros
        if frame_count % 15 == 0:
            # pasar frame a rgb
            rg_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # localizar rostros
            face_locations = fr.face_locations(rg_small_frame)

            # codificar con el frame reducido
            face_encodings = fr.face_encodings(rg_small_frame, face_locations)

        for cara_ubic, cara_codif in zip(face_locations, face_encodings):
            distancias = fr.face_distance(estudiantes_Codificados, cara_codif)
            coincidencias = fr.compare_faces(estudiantes_Codificados, cara_codif)

            indice_valor_min = numpy.argmin(distancias)

            y1, x2, y2, x1 = [v * 4 for v in cara_ubic]

            if distancias[indice_valor_min] > 0.6:
                cv2.rectangle(frame,
                              (x1, y1),
                              (x2, y2),
                              (0, 0, 255),
                              2)
                cv2.rectangle(frame,
                              (x1, y2 - 50),
                              (x2, y2),
                              (0, 0, 255),
                              cv2.FILLED)

                cv2.putText(frame,
                            "Desconocido",
                            (x1 + 10, y2 - 10),
                            cv2.FONT_HERSHEY_COMPLEX,
                            1.5,
                            (255, 255, 255),
                            5)
            else:
                nombre = nombres_estudiantes[indice_valor_min]

                cv2.rectangle(frame,
                              (x1, y1),
                              (x2, y2),
                              (0, 255, 0),
                              2)
                cv2.rectangle(frame,
                              (x1, y2 - 50),
                              (x2, y2),
                              (0, 255, 0),
                              cv2.FILLED)

                cv2.putText(frame,
                            nombre,
                            (x1 + 10, y2 - 10),
                            cv2.FONT_HERSHEY_COMPLEX,
                            1.5,
                            (0, 0, 0),
                            5)

                registrar(nombre)

        cv2.namedWindow("Imagen Web", cv2.WINDOW_NORMAL)
        cv2.imshow("Imagen Web", frame)
        k = cv2.waitKey(1)
        print(f"valor k: {k}")
        print(k & 0xFF)
        print(f"valor q: {ord('q')}")
        if k & 0xFF == ord('q'):
            break

        frame_count += 1

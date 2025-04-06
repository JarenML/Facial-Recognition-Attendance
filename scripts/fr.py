import os
from cv2 import cv2
import face_recognition as fr
import numpy
from datetime import datetime
import pymysql
from decouple import config
import pymysql.cursors

# configuracion de conexion db
conexion = pymysql.connect(
    host=config('DB_HOST'),
    user=config('DB_USER'), 
    password=config('DB_PASSWORD'),
    database=config('DB_NAME'),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


ruta = '../base/Estudiantes'
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



# Registrar en DB
def registrar(persona):
    try:
        with conexion.cursor() as cursor:
            actual = datetime.now()

            query_check = """
                SELECT COUNT(*) as total FROM base_asistencia WHERE nombre=%s
            """
            cursor.execute(query_check, (persona,))
            resultado = cursor.fetchone()

            # se insertara cuando no encuentre ya un registro existente
            if resultado['total'] == 0:

                query_insert = """
                    INSERT INTO base_asistencia (nombre, fecha, hora)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query_insert, (persona, actual.date(), actual.time()))
                conexion.commit()  # Guardar cambios
                print(f"Asistencia registrada para: {persona}")
            else:
                print(f"Asistencia ya registrada para: {persona}")
    except Exception as e:
        print(f"Error al registrar asistencia: {e}")


estudiantes_Codificados = codificar(mis_imagenes)

url = "http://192.168.1.3:8080/video"

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
conexion.close()

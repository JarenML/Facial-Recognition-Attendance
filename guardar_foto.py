import cv2
import os
from tkinter import Tk, Label, Entry, Button, StringVar, Frame
from PIL import Image, ImageTk


# Función para tomar la foto y guardarla en la carpeta 'empleados'
def tomar_foto():
    url = "http://192.168.1.4:8080/video"
    nombre = nombre_var.get().strip()  # Obtiene el nombre del Entry
    if nombre:
        # Ruta de la carpeta 'empleados' (asumiendo que ya existe)
        ruta_carpeta = "base/Estudiantes"

        # Inicializa la cámara
        cap = cv2.VideoCapture(url)
        ret, foto = cap.read()
        if ret:
            # Guardar la imagen en la carpeta 'empleados' con el nombre proporcionado
            ruta_imagen = os.path.join(ruta_carpeta, f"{nombre}.jpg")
            cv2.imwrite(ruta_imagen, foto)

            # Redimensionar la imagen antes de mostrarla
            foto = cv2.resize(foto, (300, 300))
            mostrar_imagen(foto)  # Muestra la imagen en la interfaz

        cap.release()  # Libera la cámara


def mostrar_imagen(foto):
    # Convertir la imagen de OpenCV (BGR) a un formato compatible con Tkinter (RGB)
    image = cv2.cvtColor(foto, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    # Mostrar la imagen redimensionada en el label
    panel_imagen.config(image=image)
    panel_imagen.image = image


def reiniciar():
    # Limpia la imagen mostrada y el campo de nombre
    panel_imagen.config(image="")
    nombre_var.set("")


# Interfaz gráfica con tkinter
root = Tk()
root.title("Registro de estudiantes")
root.geometry("350x600+450+20")
root.config(bg="#000000")
root.resizable(False, False)

# Crear un marco para los widgets
frame = Frame(root, bg="#89c2fb", padx=20, pady=20)
frame.pack(pady=3, padx=3)

# Variables
nombre_var = StringVar()

# Widgets con diseño
titulo = Label(frame, text="REGISTRO DE ESTUDIANTES", font=("Helvetica", 16, "bold"), bg="#89c2fb", fg="#ea480c")
titulo.pack(pady=10)

Label(frame, text="Nombre del estudiante:", font=("Helvetica", 12), bg="#89c2fb").pack(pady=10)
Entry(frame, textvariable=nombre_var, font=("Helvetica", 12), width=30, borderwidth=2, relief="solid").pack(pady=5)

Button(frame, text="Tomar foto", command=tomar_foto, font=("Helvetica", 12, "bold"),
       bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=20)
Button(frame, text="Reiniciar", command=reiniciar, font=("Helvetica", 12, "bold"),
       bg="#f44336", fg="white", padx=10, pady=5).pack(pady=5)

# Panel donde se mostrará la foto tomada
panel_imagen = Label(frame, bg="#d9d9d9", width=300, height=300, relief="solid")
panel_imagen.pack(pady=20)

# Iniciar el loop de tkinter
root.mainloop()

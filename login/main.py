from customtkinter import *
from PIL import Image
import sqlite3
import face_recognition
import numpy as np
import cv2


def on_enter_cam(event):
    event.widget.configure( height=38,width=48)

def on_leave_cam(event):
    event.widget.configure(width=50, height=40,)

def on_enter(event):
    event.widget.configure(font=("", 11, "bold"))

def on_leave(event):
    event.widget.configure(font=("", 12))


def login_user(email, password):
    conn = sqlite3.connect("../register/users.db")
    cursor = conn.cursor()


    cursor.execute("""
        SELECT validation 
        FROM users 
        WHERE email = ? AND password = ?
    """, (email, password))

    user = cursor.fetchone()
    conn.close()


    if not user:
        return "2"


    if user[0] == 0:
        return "1"


    return "3"

def handle_login():
    email = usrname_entry.get()
    password = passwd_entry.get()

    if not email or not password:
        print("Veuillez remplir tous les champs.")
        return

    if login_user(email, password)=="3":
        print("Connexion réussie !")
    elif login_user(email, password)=="1":
        print("Le compte n'est pas activé. Veuillez contacter l'administrateur.")
    else:
        print("Identifiants incorrects.")


def handle_camera_login():
    # Charger les images et les encodages depuis la base de données
    conn = sqlite3.connect("../register/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, image FROM users")
    users = cursor.fetchall()
    conn.close()

    print(f"{len(users)} utilisateurs chargés depuis la base de données.")

    known_face_encodings = []
    known_face_names = []

    for user in users:
        username, image_blob = user
        try:
            # Convertir l'image BLOB en tableau numpy
            face_encoding = np.frombuffer(image_blob, dtype=np.float32)
            known_face_encodings.append(face_encoding)
            known_face_names.append(username)
        except Exception as e:
            print(f"Erreur lors du traitement de l'utilisateur {username}: {e}")

    if not known_face_encodings:
        print("Aucun visage valide trouvé dans la base de données.")
        return

    # Capturer une image à partir de la webcam
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Erreur : Impossible d'accéder à la webcam.")
        return

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Erreur : Impossible de capturer une image depuis la webcam.")
            break

        # Dessiner un cadre vert autour de la zone de détection
        cv2.rectangle(frame, (100, 100), (500, 400), (0, 255, 0), 2)
        cv2.putText(frame, "Appuyez sur 's' pour valider ou 'q' pour quitter", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Trouver tous les visages dans l'image capturée
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        name = "Unknown"
        probability = 0.0

        if len(face_encodings) > 0:
            matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
            face_distances = face_recognition.face_distance(known_face_encodings, face_encodings[0])
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                probability = 1 - face_distances[best_match_index]

        # Afficher le nom et la probabilité
        cv2.putText(frame, f"Nom: {name}", (100, 420), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Probabilite: {probability:.2f}", (100, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Reconnaissance Faciale", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            if name != "Unknown":
                print(f"Connexion réussie ! Bienvenue, {name}.")
            else:
                print("Aucun visage reconnu.")
            break
        if key == ord('q'):
            print("Reconnaissance faciale annulée.")
            break

    video_capture.release()
    cv2.destroyAllWindows()


main = CTk()
main.title("Login Page")
main.config(bg="white")
main.geometry("900x560")
main.resizable(False, False)


bg_img = CTkImage(dark_image=Image.open("bg1.jpg"), size=(510, 560))
bg_lab = CTkLabel(main, image=bg_img, text="")
bg_lab.place(relx=0, rely=0)

bg_imgg = CTkImage(dark_image=Image.open("bg2.jpg"), size=(490, 900))

# Create CTkFrame
frame1 = CTkFrame(
    main,
    fg_color="#33aef4",
    bg_color="white",
    corner_radius=40
)
frame1.place(relx=0.52, rely=0, relwidth=0.6, relheight=1)


title = CTkLabel(frame1, text="Welcome Back!  ", bg_color="#33aef4",text_color="white", font=("", 30, "bold"))
title.place( x=70, y=100)
title = CTkLabel(frame1, text="Enter to get access to data & information", bg_color="#33aef4",text_color="white", font=("", 12))
title.place( x=70, y=140)


usrname_entry = CTkEntry(
    frame1,
    text_color="black",
    placeholder_text="Email",
    fg_color="white",
    placeholder_text_color="black",
    font=("", 12, "bold"),
    width=300,
    corner_radius=10,
    height=40,
    bg_color="#33aef4",
    border_color="white"

)
usrname_entry.place( x=70, y=190)


passwd_entry = CTkEntry(
    frame1,
    text_color="black",
    placeholder_text="Password",
    fg_color="white",
    placeholder_text_color="black",
    font=("", 12, "bold"),
    width=300,
    corner_radius=10,
    height=40,
    show="*",
    bg_color="#33aef4",
    border_color="white"

)
passwd_entry.place( x=70, y=250)

forget = CTkLabel(frame1, text="Forgot your password ?", text_color="white" , bg_color="#33aef4",cursor="hand2", font=("", 15))
forget.place( x=200, y=297)

cr_acc = CTkLabel(frame1, text="Don't have an account ?", text_color="white" ,bg_color="#33aef4", cursor="hand2", font=("", 15))
cr_acc.place( x=90, y=430)
cr_acc_register = CTkLabel(frame1, text="Register here", text_color="white" ,bg_color="#33aef4", cursor="hand2", font=("", 15,"bold"))
cr_acc_register.place( x=250, y=430)
l_btn = CTkButton(
    frame1,
    text="Login",
    font=("", 15, "bold"),
    height=40,
    width=245,
    fg_color="white",
    cursor="hand2",
    corner_radius=10,
    bg_color="#33aef4",
    text_color="#33aef4",
    hover_color="white",
    command=handle_login
)
l_btn.place( x=70, y=330)

bg_imgd = CTkImage(dark_image=Image.open("camera.jpg"), size=(48, 44))

l_btn_cam = CTkButton(
    frame1,
    image=bg_imgd,
    text="",
    compound="left",
    fg_color="transparent",
    cursor="hand2",
    bg_color="#33aef4",
    height=40,
    hover_color="#33aef4",
    width=50,
    command=handle_camera_login
)
l_btn_cam.place(x=312, y=324)


LABEL = CTkLabel(frame1, text="------------OR CREATE ACCOUNT -------------", text_color="white" , bg_color="#33aef4",cursor="hand2", font=("", 15))
LABEL.place( x=70, y=390)

forget.bind("<Enter>", on_enter)
forget.bind("<Leave>", on_leave)

cr_acc_register.bind("<Enter>",on_enter)
cr_acc_register.bind("<Leave>",on_leave)

l_btn_cam.bind("<Enter>",on_enter_cam)
l_btn_cam.bind("<Leave>",on_leave_cam)

main.mainloop()

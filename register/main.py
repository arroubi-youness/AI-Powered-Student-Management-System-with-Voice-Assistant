from customtkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import sqlite3
import face_recognition
import numpy as np



def create_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        image BLOB,
        validation BOOLEAN NOT NULL DEFAULT 0,
        level TEXT NOT NULL
    )
    ''')
    conn.commit()


def register_user(username, email, password, image_path=None):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    face_encoding = None
    if image_path:
        face_encoding = encode_face(image_path)
        if face_encoding is None:
            print("Aucun visage détecté dans l'image. Veuillez réessayer.")
            conn.close()
            return


    face_encoding_blob = sqlite3.Binary(np.array(face_encoding, dtype=np.float32).tobytes())

    cursor.execute('''
    INSERT INTO users (username, email, password, image,level) VALUES (?, ?, ?, ?,?)
    ''', (username, email, password, face_encoding_blob,"S1"))

    conn.commit()
    conn.close()
    print("Utilisateur enregistré avec succès.")

def is_student_registered(image_path):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()


    new_face_encoding = encode_face(image_path)
    if new_face_encoding is None:
        print("Aucun visage détecté dans l'image. Veuillez réessayer.")
        conn.close()
        return False


    cursor.execute("SELECT image FROM users")
    rows = cursor.fetchall()

    for row in rows:
        stored_encoding = np.frombuffer(row[0], dtype=np.float32)
        match = face_recognition.compare_faces([stored_encoding], new_face_encoding)
        if match[0]:
            conn.close()
            return True  # Visage trouvé

    conn.close()
    return False


def encode_face(image_path):

    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    if face_encodings:
        return face_encodings[0]
    else:
        return None



create_db()
def sign_up():
    global uploaded_image_path
    username = usrname_entry.get()
    email = email_entry.get()
    password = passwd_entry.get()
    password_confirm = passwd_entry_confirm.get()


    if password != password_confirm:
        print("Les mots de passe ne correspondent pas.")
        return


    if not uploaded_image_path:
        print("Veuillez télécharger une image.")
        return


    if is_student_registered(uploaded_image_path):
        print("Cet étudiant est déjà enregistré.")
    else:

        register_user(username, email, password, image_path=uploaded_image_path)


uploaded_image_path = None

def upload_image(image_label):
    global uploaded_image_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm")]
    )
    if file_path:
        uploaded_image_path = file_path
        image = Image.open(file_path)
        image.thumbnail((110, 110))

        ctk_image = CTkImage(light_image=image, dark_image=image, size=image.size)
        image_label.configure(image=ctk_image, text="")
        image_label.image = ctk_image



set_appearance_mode("System")
set_default_color_theme("blue")

def on_enter_cam(event):
    event.widget.configure( height=38,width=48)

def on_leave_cam(event):
    event.widget.configure(width=50, height=40,)

def on_enter(event):
    event.widget.configure(font=("", 11, "bold"))

def on_leave(event):
    event.widget.configure(font=("", 12))

main = CTk()
main.title("Login Page")
main.config(bg="white")
main.geometry("900x560")
main.resizable(False, False)


bg_img = CTkImage(dark_image=Image.open("bg1.jpg"), size=(510, 560))
bg_lab = CTkLabel(main, image=bg_img, text="")
bg_lab.place(relx=0, rely=0)

bg_imgg = CTkImage(dark_image=Image.open("bg2.jpg"), size=(490, 900))

frame1 = CTkFrame(
    main,
    fg_color="#33aef4",
    bg_color="white",
    corner_radius=40
)
frame1.place(relx=0.52, rely=0, relwidth=0.6, relheight=1)



title = CTkLabel(frame1, text="Welcome Dear Student!  ", bg_color="#33aef4",text_color="white", font=("", 24, "bold"))
title.place( x=97, y=28)
title = CTkLabel(frame1, text="Enter to get access to data & information", bg_color="#33aef4",text_color="white", font=("", 12))
title.place( x=115, y=65)


usrname_entry = CTkEntry(
    frame1,
    text_color="black",
    placeholder_text="Username",
    fg_color="white",
    placeholder_text_color="black",
    font=("", 12, "bold"),
    width=335,
    corner_radius=10,
    height=40,
    bg_color="#33aef4",
    border_color="white"

)
usrname_entry.place( x=55, y=230)
email_entry = CTkEntry(
    frame1,
    text_color="black",
    placeholder_text="email",
    fg_color="white",
    placeholder_text_color="black",
    font=("", 12, "bold"),
    width=330,
    corner_radius=10,
    height=40,
    bg_color="#33aef4",
    border_color="white"

)
email_entry.place( x=55, y=290)
passwd_entry = CTkEntry(
    frame1,
    text_color="black",
    placeholder_text="Password",
    fg_color="white",
    placeholder_text_color="black",
    font=("", 12, "bold"),
    width=330,
    corner_radius=10,
    height=40,
    show="*",
    bg_color="#33aef4",
    border_color="white"

)
passwd_entry.place( x=55, y=350)

passwd_entry_confirm = CTkEntry(
    frame1,
    text_color="black",
    placeholder_text="confirm Password",
    fg_color="white",
    placeholder_text_color="black",
    font=("", 12, "bold"),
    width=330,
    corner_radius=10,
    height=40,
    show="*",
    bg_color="#33aef4",
    border_color="white"
)
passwd_entry_confirm.place( x=55, y=410)


bg_imgg_user = CTkImage(dark_image=Image.open("user.jpg"),size=(70,80))

image_label = CTkLabel(
    frame1,
    image=bg_imgg_user,
    width=110,
    height=110,
    fg_color="white",
    corner_radius=20,
    text=""
)
image_label.place(x=170,y=95)

upload_button = CTkButton(
    frame1,
    text="Upload Image",
    command=lambda: upload_image(image_label),
    height=30,
    font=("", 12, "bold")

)
upload_button.place(x=242, y=460)

register_button = CTkButton(
    frame1,
    text="Sign up",
     height=35,
    width=330,
    bg_color="#33aef4",
    fg_color="white",
    text_color="#33aef4",
    corner_radius=12,
    font=("",15,"bold"),
    hover_color="white",
    cursor="hand2",
    command=sign_up
)
register_button.place(x=55,y=500)
main.mainloop()

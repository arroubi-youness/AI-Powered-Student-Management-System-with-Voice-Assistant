import tkinter
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import sqlite3
import face_recognition
import cv2
import numpy as np
from datetime import datetime
from tkinter import messagebox, filedialog
import threading

from click import command

conn = sqlite3.connect('../register/users.db')
cursor = conn.cursor()
video_capture = None
camera_thread = None

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

def display_student_results(student_id, semester):
    # Clear previous elements from the display area
    for widget in content_frame.winfo_children():
        widget.destroy()
    # Fetch all modules for the semester and match with notes for the student
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            modules.id, modules.module_name, 
            COALESCE(notes.note, 'En cours') AS grade
        FROM modules
        LEFT JOIN notes ON modules.id = notes.idmodule AND notes.iduser = ?
        WHERE modules.semester = ?
    ''', (student_id, semester))
    results = cursor.fetchall()
    conn.close()
    # Create a new frame to display results
    frame = ctk.CTkFrame(
        content_frame,
        fg_color="#D2E0FB",
        bg_color="#F0F0F0",
        corner_radius=15,
        height=550,
        width=700
    )
    frame.grid(row=0, column=0, padx=30, pady=130)
    # Title for the section
    title_label = ctk.CTkLabel(
        frame,
        text=f"Results for Semester {semester}:",
        font=("Helvetica", 14, "bold"),
        text_color="#2E86C1",
    )
    title_label.pack(pady=10)
    # Header for the results table
    header_frame = ctk.CTkFrame(frame, fg_color="#0177f2")
    header_frame.pack(fill="x", padx=5, pady=5)
    headers = ["Module", "Grade", "Status"]
    for header in headers:
        header_label = ctk.CTkLabel(
            header_frame,
            text=header,
            font=("Helvetica", 12, "bold"),
            text_color="white",
            width=200,
            anchor="center"
        )
        header_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
    # Display results in rows
    for module_id, module_name, grade in results:
        row_frame = ctk.CTkFrame(frame)
        row_frame.pack(fill="x", padx=5, pady=2)
        # Module Name
        module_label = ctk.CTkLabel(
            row_frame,
            text=module_name,
            font=("Helvetica", 12),
            width=150,
            anchor="center"
        )
        module_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        grade_label = ctk.CTkLabel(
            row_frame,
            text=str(grade),
            font=("Helvetica", 12),
            width=150,
            anchor="center"
        )
        grade_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        if grade == "En cours":
            status = "En cours"
        else:
            grade = float(grade)
            if grade < 5:
                status = "Non Valide"
            elif 5 <= grade < 10:
                status = "Ratt"
            else:
                status = "Valide"
        status_label = ctk.CTkLabel(
            row_frame,
            text=status,
            font=("Helvetica", 12),
            width=150,
            anchor="center"
        )
        status_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")
    # No results message
    if not results:
        no_results_label = ctk.CTkLabel(
            frame,
            text="No modules found for this semester.",
            font=("Helvetica", 12),
            text_color="#FF0000",
        )
        no_results_label.pack(pady=10)


def on_grades_click():
    clear_content()

    global semester_menu
    global module_menu
    frame1 = ctk.CTkFrame(
        content_frame,
        fg_color="#D2E0FB",
        bg_color="#F0F0F0",
        corner_radius=15,
        height=110,
        width=670
    )
    frame1.place(x=23, y=30)
    semester_label = ctk.CTkLabel(frame1, text="Select Semester:", font=("Arial", 14))
    semester_label.place(x=50, y=10)
    semester_menu = ctk.CTkOptionMenu(frame1, values=["S1", "S2", "S3", "S4"] )
    semester_menu.place(x=50, y=40)
    get_users_button = ctk.CTkButton(
        frame1,
        font=("Arial", 12, "bold"),
        text="Get Results",
        fg_color="#54C392",
        hover_color="#347928",command=lambda :display_student_results(101,semester_menu.get()))
    get_users_button.place(x=480,y=40)

def on_schedule_click():
    clear_content()

    global semester_menu_empoli
    frame1 = ctk.CTkFrame(
        content_frame,
        fg_color="#D2E0FB",
        bg_color="#F0F0F0",
        corner_radius=15,
        height=130,
        width=270
    )
    frame1.place(x=225, y=240)
    semester_label = ctk.CTkLabel(frame1, text="Select Semester:", font=("Arial", 14))
    semester_label.place(x=70, y=10)
    semester_menu_empoli = ctk.CTkOptionMenu(frame1, values=["S1", "S2", "S3", "S4"])
    semester_menu_empoli.place(x=70, y=40)
    bg_img_user = ctk.CTkImage(dark_image=Image.open("menu_icon/upload-regular-24.png"))
    get_users_button = ctk.CTkButton(
        frame1,
        font=("Arial", 12, "bold"),
        text="Upload Emploi",
        fg_color="#54C392",image=bg_img_user,compound=tkinter.LEFT,
        hover_color="#347928",
        command=lambda: download_image(semester_menu_empoli.get()))
    get_users_button.place(x=70, y=75)


def download_image(semester_menu):
    # Get the selected semester from the dropdown
    # Database connection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        # Query the database for the image blob
        cursor.execute('SELECT img FROM Empoloi WHERE semstre = ?', (semester_menu,))
        result = cursor.fetchone()
        if result:
            # Blob data is the first column in the result
            image_blob = result[0]
            # Prompt the user to select a file location to save the image
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if save_path:
                # Write the blob data to the selected file
                with open(save_path, 'wb') as file:
                    file.write(image_blob)
                print(f"Image saved successfully to {save_path}")
        else:
            print("No image found for the selected semester.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def presence():
    clear_content()

    def start_camera():
        global video_capture
        video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Utiliser CAP_DSHOW pour Windows
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Fonction pour arrêter la caméra
    def stop_camera():
        global video_capture
        if video_capture is not None:
            video_capture.release()
            cv2.destroyAllWindows()
            video_capture = None

    def get_student_encodings():
        cursor.execute("SELECT username, image FROM users")
        rows = cursor.fetchall()
        encodings = []
        names = []
        for row in rows:
            names.append(row[0])
            # Convertir le BLOB en tableau numpy de forme (128,)
            encoding = np.frombuffer(row[1], dtype=np.float32)  # Utiliser float32 ici
            if encoding.shape != (128,):  # Vérifier la forme de l'encodage
                raise ValueError(
                    f"Encodage facial invalide pour l'utilisateur {row[0]}. Forme attendue : (128,), forme obtenue : {encoding.shape}")
            encodings.append(encoding)
        return names, encodings
    def is_session_active():
        now = datetime.now()
        current_time = now.strftime("%H:%M")  # Format sans les secondes
        current_date = now.strftime("%Y-%m-%d")  # Format YYYY-MM-DD

        print(f"Date actuelle : {current_date}, Heure actuelle : {current_time}")

        # Convertir l'heure actuelle en minutes depuis minuit pour la comparaison
        current_time_minutes = int(current_time.split(':')[0]) * 60 + int(current_time.split(':')[1])

        # Vérifier les sessions actives en fonction de la date et de l'heure (sans les secondes)
        cursor.execute('''
        SELECT id, start_time, end_time
        FROM sessions
        WHERE date = ?
        ''', (current_date,))
        sessions = cursor.fetchall()

        for session in sessions:
            start_time = session[1]
            end_time = session[2]

            # Convertir les heures de début et de fin en minutes depuis minuit
            start_time_minutes = int(start_time.split(':')[0]) * 60 + int(start_time.split(':')[1])
            end_time_minutes = int(end_time.split(':')[0]) * 60 + int(end_time.split(':')[1])

            # Vérifier si l'heure actuelle est dans l'intervalle de la session
            if start_time_minutes <= current_time_minutes <= end_time_minutes:
                print(f"Séance trouvée : ID={session[0]}, Début={session[1]}, Fin={session[2]}")
                return {
                    'session_id': session[0],
                    'start_time': session[1],
                    'end_time': session[2]
                }

        print("Aucune séance en cours.")
        return None

    def recognize_face():
        global camera_thread


        # Vérifier si une séance est en cours
        active_session = is_session_active()
        if not active_session:
            messagebox.showinfo("Information", "Aucune séance en cours pour le moment.")
            return

        # Démarrer la caméra dans un thread séparé
        if video_capture is None:
            camera_thread = threading.Thread(target=start_camera)
            camera_thread.start()
            camera_thread.join()  # Attendre que la caméra soit initialisée

        print(
            "Positionnez votre visage devant la caméra. Appuyez sur 's' pour marquer la présence ou 'q' pour quitter.")

        while True:
            ret, frame = video_capture.read()
            if not ret:
                messagebox.showerror("Erreur", "Impossible de lire le flux vidéo.")
                break

            # Conversion en RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Détection des visages
            face_locations = face_recognition.face_locations(rgb_frame)
            if len(face_locations) > 0:
                # Calcul des encodages des visages détectés
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                # Récupération des encodages des étudiants enregistrés
                student_names, student_encodings = get_student_encodings()

                # Vérifier si des étudiants sont enregistrés
                if len(student_encodings) == 0:
                    messagebox.showwarning("Avertissement", "Aucun étudiant enregistré dans la base de données.")
                    break

                # Comparaison des encodages détectés avec ceux des étudiants
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    face_distances = face_recognition.face_distance(student_encodings, face_encoding)

                    # Vérifier si des distances ont été calculées
                    if len(face_distances) == 0:
                        messagebox.showwarning("Avertissement", "Impossible de comparer les visages.")
                        continue

                    best_match_index = np.argmin(face_distances)
                    best_match_distance = face_distances[best_match_index]

                    # Seuil de tolérance pour la reconnaissance
                    tolerance = 0.5
                    if best_match_distance <= tolerance:
                        recognized_name = student_names[best_match_index]
                        probability = 1 - best_match_distance

                        # Dessiner un cadre vert autour du visage détecté
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                        # Afficher le nom et la probabilité au-dessus du rectangle
                        text = f"{recognized_name} ({probability:.2f})"
                        cv2.putText(frame, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Affichage du flux vidéo
            cv2.imshow("Reconnaissance du visage", frame)

            # Attendre une touche
            key = cv2.waitKey(30) & 0xFF
            if key == ord('s'):  # Appuyer sur 's' pour marquer la présence
                if len(face_locations) == 0:
                    messagebox.showwarning("Avertissement",
                                           "Aucun visage détecté. Veuillez vous positionner correctement devant la caméra.")
                    continue

                # Calcul des encodages des visages détectés
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                if len(face_encodings) == 0:
                    messagebox.showerror("Erreur", "Impossible de calculer l'encodage du visage. Veuillez réessayer.")
                    continue

                # Récupération des encodages des étudiants enregistrés
                student_names, student_encodings = get_student_encodings()

                # Vérifier si des étudiants sont enregistrés
                if len(student_encodings) == 0:
                    messagebox.showwarning("Avertissement", "Aucun étudiant enregistré dans la base de données.")
                    break

                # Comparaison des encodages détectés avec ceux des étudiants
                for i, face_encoding in enumerate(face_encodings):
                    face_distances = face_recognition.face_distance(student_encodings, face_encoding)

                    # Vérifier si des distances ont été calculées
                    if len(face_distances) == 0:
                        messagebox.showwarning("Avertissement", "Impossible de comparer les visages.")
                        continue

                    best_match_index = np.argmin(face_distances)
                    best_match_distance = face_distances[best_match_index]

                    # Seuil de tolérance pour la reconnaissance
                    tolerance = 0.5
                    if best_match_distance <= tolerance:
                        recognized_name = student_names[best_match_index]
                        messagebox.showinfo("Succès",
                                            f"Présence marquée pour : {recognized_name} (distance : {best_match_distance:.2f})")

                        # Récupérer l'ID de l'étudiant reconnu
                        cursor.execute("SELECT id FROM users WHERE username = ?", (recognized_name,))
                        student_id = cursor.fetchone()[0]

                        # Marquer la présence dans la table presence
                        cursor.execute('''
                        INSERT INTO presence (session_id, student_id, date, status)
                        VALUES (?, ?, ?, ?)
                        ''', (active_session['session_id'], student_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              "présent"))
                        conn.commit()
                    else:
                        messagebox.showwarning("Avertissement", "Visage inconnu détecté.")
                break

            elif key == ord('q'):  # Appuyer sur 'q' pour quitter
                break

        # Fermer la fenêtre de la caméra et arrêter la caméra
        cv2.destroyAllWindows()
        stop_camera()
    recognize_button = ctk.CTkButton(content_frame, text="Reconnaître et marquer la présence",command=recognize_face)
    recognize_button.place(x=50,y=70)
    recognize_button = ctk.CTkButton(content_frame, text="afiche l historique")
    recognize_button.place(x=500, y=70)


def create_circular_image(image_path, size):
    # Ouvrir l'image et la redimensionner
    image = Image.open(image_path)
    image = image.resize((size, size), Image.Resampling.LANCZOS)

    # Créer un masque circulaire
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    # Appliquer le masque à l'image
    circular_image = Image.new("RGBA", (size, size))
    circular_image.paste(image, (0, 0), mask)
    return circular_image


root = ctk.CTk()
root.title("Gestion des Étudiants")
root.geometry("1000x600")
root.resizable(False, False)

menu_frame = ctk.CTkFrame(root, width=310, height=600, fg_color="#33aef4", bg_color="#F0F0F0", corner_radius=35)
menu_frame.place(x=-28, y=0)

try:
    circular_image = create_circular_image("bg1.jpg", 150)
    photo = ImageTk.PhotoImage(circular_image)
except FileNotFoundError:
    print("Erreur : L'image n'a pas été trouvée. Vérifiez le chemin.")
    photo = None

if photo:
    image_label = ctk.CTkLabel(menu_frame, image=photo, text="", fg_color="transparent")
    image_label.place(x=90, y=10)  # Position fixe pour l'image (x=50, y=30)
else:
    error_label = ctk.CTkLabel(menu_frame, text="Image non trouvée", font=("Helvetica", 12), fg_color="transparent")
    error_label.place(x=50, y=50)  # Position fixe pour le message d'erreur

# Titre de l'application dans le menu
title_label = ctk.CTkLabel(menu_frame, text="OULAID MOHAMMED", font=("Helvetica", 18, "bold"), fg_color="transparent",text_color="white")
title_label.place(x=76, y=170)  # Position fixe pour le titre (x=50, y=200)

# Boutons du menu (style moderne)
button_style = {"font": ("Helvetica", 14, "bold"),"anchor":"w", "width": 200, "height": 40, "corner_radius": 10,"fg_color": "transparent","text_color":"white"}
logout_button_style = {
    "font": ("Helvetica", 14,"bold"),
    "width": 200,
    "height": 40,
    "corner_radius": 10,
    "fg_color": "#FF0000",  # Rouge vif
    "hover_color": "#CC0000",  # Rouge foncé au survol
    "text_color": "white"  # Texte en blanc pour un bon contraste
}
bg_img_user = ctk.CTkImage(dark_image=Image.open("menu_icon/user-circle-regular-24.png"))
bg_img_book = ctk.CTkImage(dark_image=Image.open("menu_icon/book-solid-24.png"))
bg_img_notes = ctk.CTkImage(dark_image=Image.open("menu_icon/edit-alt-solid-24.png"))
bg_img_time = ctk.CTkImage(dark_image=Image.open("menu_icon/time-regular-24.png"))
bg_img_user_profil = ctk.CTkImage(dark_image=Image.open("menu_icon/user-solid-24.png"))

bg_img_logout=ctk.CTkImage(dark_image=Image.open("menu_icon/log-out-circle-regular-24.png"))


# Position fixe pour chaque bouton
student_button = ctk.CTkButton(menu_frame, text="Presence", command=presence, font=("Helvetica", 14, "bold"), width=200, anchor="w",height=40, corner_radius= 10,fg_color= "transparent",text_color="white",image=bg_img_user,compound=tkinter.LEFT)
student_button.place(x=65, y=370)
course_button = ctk.CTkButton(menu_frame, text="Voice Assistant", **button_style,image=bg_img_notes,compound=tkinter.LEFT)
course_button.place(x=65, y=310)

schedule_button = ctk.CTkButton(menu_frame, text="Emploi du temps",command=on_schedule_click, **button_style,image=bg_img_time,compound=tkinter.LEFT)
schedule_button.place(x=65, y=250) # Position (x=35, y=370)

grades_button = ctk.CTkButton(menu_frame, text="Notes", **button_style,command=on_grades_click,image=bg_img_notes,compound=tkinter.LEFT)
grades_button.place(x=65, y=430)



settings_button = ctk.CTkButton(menu_frame,text="log out", **logout_button_style,image=bg_img_logout,compound=tkinter.LEFT)
settings_button.place(x=65, y=550)  # Position (x=35, y=610)

# Cadre pour le contenu (à droite)
content_frame = ctk.CTkFrame(root, width=720, height=600, fg_color="#F0F0F0", corner_radius=0)
content_frame.place(x=282, y=0)  # Position fixe à droite

# Lancement de l'application
root.mainloop()
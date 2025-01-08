import tkinter
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk
from datetime import datetime
from plyer import notification
from tkinter import messagebox
import sqlite3




conn = sqlite3.connect('../register/users.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS presence (
    id INTEGER PRIMARY KEY,
    session_id INTEGER,
    student_id INTEGER,
    date TEXT,
    status TEXT,
    FOREIGN KEY (student_id) REFERENCES users (id),
    FOREIGN KEY (session_id) REFERENCES sessions (id)
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL
)
''')
conn.commit()


def Presence():
    def save_session():
        selected_day = day_menu.get()
        selected_month = month_menu.get()
        selected_year = year_menu.get()
        start_time = start_time_entry.get()
        end_time = end_time_entry.get()

        if not (selected_day and selected_month and selected_year and start_time and end_time):
            show_toast("Erreur", "Tous les champs sont obligatoires.")
            return

        try:
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")
        except ValueError:
            show_toast("Erreur", "Les heures doivent être au format HH:MM.")
            return

        # Construire la date au format YYYY-MM-DD
        date = f"{selected_year}-{selected_month.zfill(2)}-{selected_day.zfill(2)}"

        # Insérer la séance dans la base de données
        cursor.execute('''
            INSERT INTO sessions (date, start_time, end_time)
            VALUES (?, ?, ?)
        ''', (date, start_time, end_time))
        conn.commit()

        session_id = cursor.lastrowid
        print(f"Séance créée : ID={session_id}, Date={date}, Début={start_time}, Fin={end_time}")
        show_toast("Succès", f"Séance créée pour le {date} de {start_time} à {end_time}.")

        conn.commit()

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

    def mark_absent_for_today():
        # Récupérer la date du jour au format "YYYY-MM-DD"
        today = datetime.now().strftime("%Y-%m-%d")

        # Récupérer les informations de la session active
        session_info = is_session_active()
        if not session_info:
            messagebox.showwarning("Avertissement", "Aucune session active trouvée pour aujourd'hui.")
            return

        # Extraire l'ID de la session du dictionnaire
        session_id = session_info['session_id']

        # Récupérer tous les étudiants
        cursor.execute("SELECT id, username FROM users")
        students = cursor.fetchall()

        # Pour chaque étudiant, vérifier s'il a marqué sa présence aujourd'hui
        for student_id, student_name in students:
            cursor.execute('''
            SELECT id FROM presence
            WHERE student_id = ? AND date LIKE ? AND session_id = ?
            ''', (student_id, f"{today}%", session_id))
            attendance_record = cursor.fetchone()

            # Si l'étudiant n'a pas de présence pour aujourd'hui, marquer comme absent
            if not attendance_record:
                cursor.execute('''
                INSERT INTO presence (session_id, student_id, date, status)
                VALUES (?, ?, ?, ?)
                ''', (session_id, student_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "absent"))
                conn.commit()
                print(f"Absence marquée pour {student_name} (ID: {student_id})")

        messagebox.showinfo("Succès", "Les absences ont été marquées pour les étudiants non présents aujourd'hui.")


    def get_available_sessions():
        cursor.execute('''
        SELECT id, date, start_time, end_time
        FROM sessions
        ''')
        rows = cursor.fetchall()

        # Construire une liste de dictionnaires contenant les informations des séances
        sessions = [
            {
                'session_id': row[0],
                'date': row[1],
                'start_time': row[2],
                'end_time': row[3]
            }
            for row in rows
        ]

        # Trier les séances par date et heure de début
        sessions = sorted(sessions, key=lambda x: (x['date'], x['start_time']))

        return sessions

    # Fonction pour afficher les présences
    def view_attendance():
        # Récupérer les séances disponibles
        available_sessions = get_available_sessions()
        if not available_sessions:
            messagebox.showinfo("Information", "Aucune donnée de présence disponible.")
            return

        # Effacer les anciens éléments dans le cadre d'affichage
        for widget in attendance_scrollable_frame.winfo_children():
            widget.destroy()

        # Titre pour la section des séances disponibles
        title_label = ctk.CTkLabel(
            attendance_scrollable_frame,
            text="Sélectionnez une séance :",
            font=("Helvetica", 14, "bold"),
            text_color="#2E86C1",  # Couleur bleue pour le titre
        )
        title_label.pack(pady=10)

        # Afficher chaque séance sous forme de bouton stylisé
        for session in available_sessions:
            session_button = ctk.CTkButton(
                attendance_scrollable_frame,
                text=f"{session['date']} - {session['start_time']} à {session['end_time']}",
                font=("Helvetica", 12),
                fg_color="#4CAF50",  # Couleur verte pour les boutons
                hover_color="#45a049",  # Couleur au survol
                command=lambda s=session: show_attendance_for_date(s),  # Passer la séance sélectionnée
            )
            session_button.pack(pady=5, padx=10, fill="x")

    # Fonction pour afficher les présences et absences pour une date spécifique
    def show_attendance_for_date(selected_session):
        # Effacer les anciens éléments dans le cadre d'affichage
        for widget in attendance_scrollable_frame.winfo_children():
            widget.destroy()

        # Récupérer les enregistrements de présence pour la séance sélectionnée
        cursor.execute('''
        SELECT users.username, presence.date, presence.status
        FROM presence
        JOIN users ON presence.student_id = users.id
        WHERE presence.session_id = ?
        ''', (selected_session['session_id'],))  # Utiliser l'ID de la séance pour filtrer
        rows = cursor.fetchall()

        # Titre pour la section des présences/absences
        title_label = ctk.CTkLabel(
            attendance_scrollable_frame,
            text=f"Présences et absences pour la séance du {selected_session['date']} :",
            font=("Helvetica", 14, "bold"),
            text_color="#2E86C1",  # Couleur bleue pour le titre
        )
        title_label.pack(pady=10)

        # Créer un cadre pour les en-têtes
        header_frame = ctk.CTkFrame(attendance_scrollable_frame, fg_color="#0177f2")
        header_frame.pack(fill="x", padx=5, pady=5)

        # En-têtes du tableau
        headers = ["Étudiant", "Date", "Statut"]
        for header in headers:
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Helvetica", 12, "bold"),
                text_color="white",  # Texte en blanc
                width=150,
                anchor="center"
            )
            header_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        # Remplir le tableau avec les données
        for row in rows:
            # Créer un cadre pour chaque ligne
            row_frame = ctk.CTkFrame(attendance_scrollable_frame)
            row_frame.pack(fill="x", padx=5, pady=2)

            # Nom de l'étudiant
            name_label = ctk.CTkLabel(
                row_frame,
                text=row[0],
                font=("Helvetica", 12),
                width=150,
                anchor="center"
            )
            name_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")

            # Date
            date_label = ctk.CTkLabel(
                row_frame,
                text=row[1],
                font=("Helvetica", 12),
                width=150,
                anchor="center"
            )
            date_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")

            # Statut (présent ou absent)
            status_label = ctk.CTkLabel(
                row_frame,
                text=row[2],
                font=("Helvetica", 12, "bold"),
                width=150,
                anchor="center",
                corner_radius=5,
                fg_color="#4CAF50" if row[2].lower() == "présent" else "#FF5252",
                # Vert pour présent, rouge pour absent
                text_color="white"  # Texte en blanc
            )
            status_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")

    def show_toast(title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Presence App",
            timeout=5  # Durée d'affichage de la notification en secondes
        )

    # Effacer les widgets précédents
    clear_content()

    title_label = ctk.CTkLabel(
        content_frame,
        text="Création d'une nouvelle séance",
        font=("Helvetica", 18, "bold"),
    )
    title_label.place(x=200, y=20)

    date_label = ctk.CTkLabel(content_frame, text="Date de la séance :", font=("Helvetica", 14))
    date_label.place(x=20, y=80)

    days = [str(i).zfill(2) for i in range(1, 32)]
    months = [str(i).zfill(2) for i in range(1, 13)]
    years = [str(i) for i in range(2023, 2035)]

    day_menu = ttk.Combobox(content_frame, values=days, width=5, state="readonly")
    day_menu.set("Jour")
    day_menu.place(x=20, y=110)

    month_menu = ttk.Combobox(content_frame, values=months, width=5, state="readonly")
    month_menu.set("Mois")
    month_menu.place(x=90, y=110)

    year_menu = ttk.Combobox(content_frame, values=years, width=8, state="readonly")
    year_menu.set("Année")
    year_menu.place(x=160, y=110)

    # Heure de début
    start_time_label = ctk.CTkLabel(content_frame, text="Heure de début (HH:MM) :", font=("Helvetica", 14))
    start_time_label.place(x=280, y=80)
    start_time_entry = ctk.CTkEntry(content_frame, width=200, placeholder_text="Ex : 08:30")
    start_time_entry.place(x=280, y=110)

    # Heure de fin
    end_time_label = ctk.CTkLabel(content_frame, text="Heure de fin (HH:MM) :", font=("Helvetica", 14))
    end_time_label.place(x=500, y=80)
    end_time_entry = ctk.CTkEntry(content_frame, width=200, placeholder_text="Ex : 10:30")
    end_time_entry.place(x=500, y=110)

    # Bouton de sauvegarde
    save_button = ctk.CTkButton(
        content_frame,
        text="Créer la séance",
        command=save_session,
        width=200,
        fg_color="green",
        hover_color="darkgreen",
    )
    save_button.place(x=240, y=170)

    title_pre = ctk.CTkLabel(
        content_frame,
        text="voire les presence",
        font=("Helvetica", 18, "bold"),
    )
    title_pre.place(x=250, y=230)

    view_button = ctk.CTkButton(content_frame, text="Afficher les présences", command=view_attendance)
    view_button.place(x=100,y=270)

    mark_absent_button = ctk.CTkButton(content_frame, text="Marquer les absences",command=mark_absent_for_today)
    mark_absent_button.place(x=450,y=270)

    attendance_scrollable_frame = ctk.CTkScrollableFrame(content_frame, fg_color="#ffffff", width=680, height=280)
    attendance_scrollable_frame.place(x=5,y=310)



def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

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
student_button = ctk.CTkButton(menu_frame, text="Presence", command=Presence, font=("Helvetica", 14, "bold"), width=200, anchor="w",height=40, corner_radius= 10,fg_color= "transparent",text_color="white",image=bg_img_user,compound=tkinter.LEFT)
student_button.place(x=65, y=370)
course_button = ctk.CTkButton(menu_frame, text="Voice Assitant",  **button_style,image=bg_img_book,compound=tkinter.LEFT)
course_button.place(x=65, y=310)   # Position (x=35, y=250)
 # Position (x=35, y=310)

schedule_button = ctk.CTkButton(menu_frame, text="Emploi du temps",  **button_style,image=bg_img_time,compound=tkinter.LEFT)
schedule_button.place(x=65, y=250) # Position (x=35, y=370)

grades_button = ctk.CTkButton(menu_frame, text="Notes",  **button_style,image=bg_img_notes,compound=tkinter.LEFT)
grades_button.place(x=65, y=430)# Position (x=35, y=430)

  # Position (x=35, y=490)


settings_button = ctk.CTkButton(menu_frame,text="log out",  **logout_button_style,image=bg_img_logout,compound=tkinter.LEFT)
settings_button.place(x=65, y=550)  # Position (x=35, y=610)

# Cadre pour le contenu (à droite)
content_frame = ctk.CTkFrame(root, width=720, height=600, fg_color="#F0F0F0", corner_radius=0)
content_frame.place(x=282, y=0)  # Position fixe à droite

# Lancement de l'application
root.mainloop()
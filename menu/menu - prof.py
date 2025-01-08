import tkinter
from tkinter import filedialog
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
        command=lambda: upload_image(content_frame))
    get_users_button.place(x=70, y=75)


def get_modules(semester):
    cursor.execute('SELECT module_name FROM modules WHERE semester = ?', (semester,))
    modules = cursor.fetchall()
    return [module[0] for module in modules]
def update_module_menu(event=None):

    selected_semester = semester_menu.get()

    if selected_semester:

        modules = get_modules(selected_semester)

        module_menu.configure(values=modules)

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
    semester_label.place(x=50,y=10)

    semester_menu = ctk.CTkOptionMenu(frame1, values=["S1", "S2", "S3", "S4"], command=update_module_menu)
    semester_menu.place(x=50,y=40)

    module_label = ctk.CTkLabel(frame1, text="Select Module:", font=("Arial", 14))
    module_label.place(x=480,y=10)

    module_menu = ctk.CTkOptionMenu(frame1, values = [])
    module_menu.place(x=480,y=40)


    get_users_button = ctk.CTkButton(
        frame1,
        font=("Arial", 12, "bold"),
        text="Get Students",
        fg_color="#54C392",
        hover_color="#347928",
        command=lambda: get_users_by_module(semester_menu.get(), module_menu.get()) )
    get_users_button.place(x=267,y=75)




def display_users_with_grades(users, module,module_id):

    for widget in content_frame.winfo_children():
        widget.destroy()


    frame6 = ctk.CTkFrame(
        content_frame,
        fg_color="#D2E0FB",
        bg_color="#F0F0F0",
        corner_radius=15,
        height=550,
        width=700
    )
    frame6.grid(row=0, column=0, padx=30, pady=20)


    canvas = ctk.CTkCanvas(frame6, width=670, height=500)
    canvas.grid(row=0, column=0, sticky="nsew")


    scrollbar = ctk.CTkScrollbar(frame6, orientation="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")


    canvas.configure(yscrollcommand=scrollbar.set)


    content_frame_in_canvas = ctk.CTkFrame(canvas)


    canvas.create_window((0, 0), window=content_frame_in_canvas, anchor="nw")


    title_label = ctk.CTkLabel(
        content_frame_in_canvas,
        text=f"Users for {module}:",
        font=("Helvetica", 14, "bold"),
        text_color="#33aef4",
    )
    title_label.pack(pady=10)


    header_frame = ctk.CTkFrame(content_frame_in_canvas, fg_color="#33aef4")
    header_frame.pack(fill="x", padx=5, pady=5)


    headers = ["ID", "Username", "Module", "Grade"]
    for header in headers:
        header_label = ctk.CTkLabel(
            header_frame,
            text=header,
            font=("Helvetica", 12, "bold"),
            text_color="white",
            width=150,
            anchor="center",
            fg_color="#33aef4"
        )
        header_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")


    grade_inputs = []
    for user in users:
        user_id, username, _ = user

        row_frame = ctk.CTkFrame(content_frame_in_canvas)
        row_frame.pack(fill="x", padx=5, pady=2)


        id_label = ctk.CTkLabel(
            row_frame,
            text=str(user_id),
            font=("Helvetica", 12),
            width=150,
            anchor="center",
        )
        id_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")


        name_label = ctk.CTkLabel(
            row_frame,
            text=username,
            font=("Helvetica", 12),
            width=150,
            anchor="center"
        )
        name_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")


        module_label = ctk.CTkLabel(
            row_frame,
            text=module,
            font=("Helvetica", 12),
            width=150,
            anchor="center"
        )
        module_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")


        grade_entry = ctk.CTkEntry(row_frame, placeholder_text="Enter Grade")
        grade_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        grade_inputs.append(grade_entry)


    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


    def on_save_grades():
        for i, user in enumerate(users):
            user_id = user[0]
            grade = grade_inputs[i].get()
            if grade:
                cursor.execute(''' 
                    INSERT INTO notes (iduser, idmodule, note) 
                    VALUES (?, ?, ?)
                ''', (user_id, module_id, grade))
                conn.commit()


    save_button = ctk.CTkButton(
        content_frame, text="Save Grades", command=on_save_grades, fg_color="#4CAF50", hover_color="#45a049"
    )
    save_button.grid(row=1,column=0)
def get_users_by_module(semester, module_name):


    # Fetch the id of the module
    cursor.execute('''
       SELECT id
       FROM modules
       WHERE module_name = ?
    ''', (module_name,))
    module_data = cursor.fetchone()

    if module_data is None:
        print(f"No module found with the name '{module_name}'.")
        return []

    module_id = module_data[0]  # Extract the module id

    # Fetch users by semester
    cursor.execute('''
       SELECT id, username, email
       FROM users
       WHERE level = ?
    ''', (semester,))
    users = cursor.fetchall()

    # Call the display function with users and module id
    display_users_with_grades(users, module_name, module_id)
    return users

def on_messages_click():
    clear_content()
    content_label = ctk.CTkLabel(content_frame, text="Gestion des messages", font=("Helvetica", 16))
    content_label.place(relx=0.5, rely=0.5, anchor="center")

def on_profile_click():
    clear_content()
    content_label = ctk.CTkLabel(content_frame, text="Gestion du profil", font=("Helvetica", 16))
    content_label.place(relx=0.5, rely=0.5, anchor="center")

def on_settings_click():
    clear_content()
    content_label = ctk.CTkLabel(content_frame, text="Configuration de l'application", font=("Helvetica", 16))
    content_label.place(relx=0.5, rely=0.5, anchor="center")

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()




uploaded_image_path = None  # Global variable to store the uploaded image path


def upload_image(content_frame):
    global uploaded_image_path

    global  image_blob
    def insert_into_emploi(image,semester):

        # Connect to the SQLite database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Create the table if it doesn't exist


        # Insert the image and string into the table
        cursor.execute(f'''
            INSERT INTO Empoloi (img, semstre) 
            VALUES (?, ?)
        ''', (image, semester))

        conn.commit()

    # Allow user to select an image file
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm")]
    )





    if file_path:
        uploaded_image_path = file_path
        with open(file_path, "rb") as file:
            image_blob = file.read()
        # Open the image using PIL
        image = Image.open(file_path)
        image.thumbnail((570, 440))


        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)


        image_label = ctk.CTkLabel(
            content_frame,
            image=ctk_image,
            width=570,
            height=440,
            fg_color="white",
            corner_radius=20,
            text=""
        )
        image_label.image = ctk_image
        image_label.place(x=60, y=95)

        # Position the label
        get_users_button = ctk.CTkButton(
            content_frame,
            font=("Arial", 13, "bold"),
            text="Save ",
            fg_color="#54C392",
            hover_color="#347928",
            command=lambda: insert_into_emploi(image_blob,semester_menu_empoli.get()))
        get_users_button.place(x=297, y=550)

def create_circular_image(image_path, size):

    image = Image.open(image_path)
    image = image.resize((size, size), Image.Resampling.LANCZOS)


    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)


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
    image_label.place(x=90, y=10)
else:
    error_label = ctk.CTkLabel(menu_frame, text="Image non trouvée", font=("Helvetica", 12), fg_color="transparent")
    error_label.place(x=50, y=50)


title_label = ctk.CTkLabel(menu_frame, text="OULAID MOHAMMED", font=("Helvetica", 18, "bold"), fg_color="transparent",text_color="white")
title_label.place(x=76, y=170)


button_style = {"font": ("Helvetica", 14, "bold"),"anchor":"w", "width": 200, "height": 40, "corner_radius": 10,"fg_color": "transparent","text_color":"white"}
logout_button_style = {
    "font": ("Helvetica", 14,"bold"),
    "width": 200,
    "height": 40,
    "corner_radius": 10,
    "fg_color": "#FF0000",
    "hover_color": "#CC0000",
    "text_color": "white"
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


schedule_button = ctk.CTkButton(menu_frame, text="Emploi du temps", command=on_schedule_click, **button_style,image=bg_img_time,compound=tkinter.LEFT)
schedule_button.place(x=65, y=250)

grades_button = ctk.CTkButton(menu_frame, text="Notes", command=on_grades_click, **button_style,image=bg_img_notes,compound=tkinter.LEFT)
grades_button.place(x=65, y=430)




settings_button = ctk.CTkButton(menu_frame,text="log out",  **logout_button_style,image=bg_img_logout,compound=tkinter.LEFT)
settings_button.place(x=65, y=550)  # Position (x=35, y=610)
settings_button = ctk.CTkButton(menu_frame,text="log out", command=on_settings_click, **logout_button_style,image=bg_img_logout,compound=tkinter.LEFT)
settings_button.place(x=65, y=550)


content_frame = ctk.CTkFrame(root, width=720, height=600, fg_color="#F0F0F0", corner_radius=0)
content_frame.place(x=282, y=0)




root.mainloop()
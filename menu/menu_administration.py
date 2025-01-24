import tkinter

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import sqlite3



def display_teachers():
    conn = sqlite3.connect("../register/users.db")
    cursor = conn.cursor()

    for widget in content_frame.winfo_children():
        widget.destroy()

    frame = ctk.CTkFrame(
        content_frame,
        fg_color="#D2E0FB",
        bg_color="#F0F0F0",

        corner_radius=15,
        height=550,
        width=700
    )
    frame.grid(row=0, column=0, padx=30, pady=20)

    canvas = ctk.CTkCanvas(frame, width=670, height=570)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    canvas.configure(yscrollcommand=scrollbar.set)

    content_frame_in_canvas = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=content_frame_in_canvas, anchor="nw")

    title_label = ctk.CTkLabel(
        content_frame_in_canvas,
        text="Teachers List",
        font=("Helvetica", 14, "bold"),
        text_color="#33aef4",
    )
    title_label.pack(pady=10)

    header_frame = ctk.CTkFrame(content_frame_in_canvas, fg_color="#33aef4")
    header_frame.pack(fill="x", padx=5, pady=5)

    headers = ["ID", "Name", "Semester", "Module", "Remove"]
    for header in headers:
        header_label = ctk.CTkLabel(
            header_frame,
            text=header,
            font=("Helvetica", 12, "bold"),
            text_color="white",
            anchor="center",
        )
        header_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")

    cursor.execute("SELECT id, fullName, semester, module FROM Teachers")
    teachers = cursor.fetchall()

    for teacher in teachers:
        teacher_id, name, semester, module = teacher

        row_frame = ctk.CTkFrame(content_frame_in_canvas)
        row_frame.pack(fill="x", padx=5, pady=2)

        id_label = ctk.CTkLabel(
            row_frame,
            text=str(teacher_id),
            font=("Helvetica", 12),
            anchor="center",
            width=120
        )
        id_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        name_label = ctk.CTkLabel(
            row_frame,
            text=name,
            font=("Helvetica", 12),
            anchor="center",
            width=120
        )
        name_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        semester_label = ctk.CTkLabel(
            row_frame,
            text=semester,
            font=("Helvetica", 12),
            anchor="center",
            width=120
        )
        semester_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        module_label = ctk.CTkLabel(
            row_frame,
            text=module,
            font=("Helvetica", 12),
            anchor="center",
            width=120
        )
        module_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        delete_button = ctk.CTkButton(
            row_frame,
            text="Delete",
            width=95,
            fg_color="RED",
            command=lambda sid=teacher_id: delete_teacher(sid)
        )
        delete_button.pack(side="left", padx=5, pady=5, fill="x")

    canvas.update_idletasks()


    canvas.config(scrollregion=canvas.bbox("all"))


def delete_teacher(teacher_id):
    # Show confirmation dialog
    confirm = messagebox.askyesno(
        "Confirm Deletion",
        "Are you sure you want to delete this teacher?"
    )


    if confirm:
        conn = sqlite3.connect("../register/users.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Teachers WHERE id = ?", (teacher_id,))
        conn.commit()
        cursor.close()
        display_teachers()



def delete_student(student_id):
    conn = sqlite3.connect("../register/users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Teachers WHERE id = ?", (student_id,))
    conn.commit()
    display_teachers()  # Refresh the display



def display_students():
    conn = sqlite3.connect("../register/users.db")
    cursor = conn.cursor()

    for widget in content_frame.winfo_children():
        widget.destroy()


    frame = ctk.CTkFrame(
        content_frame,
        fg_color="#D2E0FB",
        bg_color="#F0F0F0",
        corner_radius=15,
        height=550,
        width=700
    )
    frame.grid(row=0, column=0, padx=30, pady=20)


    canvas = ctk.CTkCanvas(frame, width=670, height=570)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = ctk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    canvas.configure(yscrollcommand=scrollbar.set)


    content_frame_in_canvas = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=content_frame_in_canvas, anchor="nw")


    title_label = ctk.CTkLabel(
        content_frame_in_canvas,
        text="Student List",
        font=("Helvetica", 14, "bold"),
        text_color="#33aef4",
    )
    title_label.pack(pady=10)


    header_frame = ctk.CTkFrame(content_frame_in_canvas, fg_color="#33aef4")
    header_frame.pack(fill="x", padx=5, pady=5)

    headers = ["ID", "Name", "Email", "Level","Remove"]
    for header in headers:
        header_label = ctk.CTkLabel(
            header_frame,
            text=header,
            font=("Helvetica", 12, "bold"),
            text_color="white",
            anchor="center",
        )
        header_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")


    cursor.execute("SELECT id, username, email, level FROM users")
    students = cursor.fetchall()


    for student in students:
        student_id, name, email, level = student

        row_frame = ctk.CTkFrame(content_frame_in_canvas)
        row_frame.pack(fill="x", padx=5, pady=2)


        id_label = ctk.CTkLabel(
            row_frame,
            text=str(student_id),
            font=("Helvetica", 12),
            anchor="center",
            width=120
        )
        id_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")


        name_label = ctk.CTkLabel(
            row_frame,
            text=name,
            font=("Helvetica", 12),
            anchor="center",
            width=120
        )
        name_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")


        email_label = ctk.CTkLabel(
            row_frame,
            text=email,
            font=("Helvetica", 12),
            anchor="center",
            width=120
        )
        email_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")


        level_label = ctk.CTkLabel(
            row_frame,
            text=level,
            font=("Helvetica", 12),
            anchor="center",
            width=120
        )
        level_label.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        grade_button = ctk.CTkButton(
            row_frame,
            text="Delete",
            width=90,
           fg_color="RED",
            command=lambda sid=student_id: delete_student(sid)
        )
        grade_button.pack(side="left", padx=5, pady=5, fill="x")

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    def delete_student(student_id):

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this student?"
        )


        if confirm:
            conn = sqlite3.connect("../register/users.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (student_id,))
            conn.commit()
            cursor.close()
            display_students()

def on_student_click():
    clear_content()
    content_label = ctk.CTkLabel(content_frame, text="Gestion des étudiants", font=("Helvetica", 16))
    content_label.place(relx=0.5, rely=0.5, anchor="center")

def on_course_click():
    clear_content()
    content_label = ctk.CTkLabel(content_frame, text="Gestion des cours", font=("Helvetica", 16))
    content_label.place(relx=0.5, rely=0.5, anchor="center")




def validation():
    def update_account_status(user_id, status):
        conn = sqlite3.connect("../register/users.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET validation = ? WHERE id = ?", (status, user_id))
        conn.commit()
        conn.close()
        load_users()

    def load_users():
        for widget in content_frame.winfo_children():
            widget.destroy()

        title_label = ctk.CTkLabel(
            content_frame,
            text="Validation des comptes utilisateurs",
            font=("Helvetica", 20, "bold"),
            text_color="black",
        )
        title_label.pack(pady=10)

        # Scrollable frame for user list
        scrollable_frame = ctk.CTkScrollableFrame(content_frame, width=680, height=500)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        conn = sqlite3.connect("../register/users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, validation FROM users")
        users = cursor.fetchall()
        conn.close()

        if not users:
            empty_label = ctk.CTkLabel(
                scrollable_frame,
                text="Aucun utilisateur trouvé.",
                font=("Helvetica", 14),
                text_color="gray",
            )
            empty_label.pack(pady=10)
            return

        for user in users:
            user_id, username, email, validated = user
            if validated:
                status_text = "✔ Validé"
                status_color = "green"
                frame_color = "#d4edda"
            else:
                status_text = "✘ Non validé"
                status_color = "red"
                frame_color = "#f8d7da"

            user_frame = ctk.CTkFrame(scrollable_frame, width=650, height=100, corner_radius=10, fg_color=frame_color)
            user_frame.pack(pady=10, padx=10)

            info_label = ctk.CTkLabel(
                user_frame,
                text=f"{username} ",
                font=("Helvetica", 16),
                anchor="w",
            )
            info_label.place(x=20, y=20)

            status_label = ctk.CTkLabel(
                user_frame,
                text=status_text,
                font=("Helvetica", 14),
                text_color=status_color,
            )
            status_label.place(x=500, y=20)

            activate_button = ctk.CTkButton(
                user_frame,
                text="Activer",
                width=100,
                command=lambda uid=user_id: update_account_status(uid, 1),
            )
            activate_button.place(x=430, y=60)

            deactivate_button = ctk.CTkButton(
                user_frame,
                text="Désactiver",
                width=100,
                fg_color="red",
                hover_color="darkred",
                command=lambda uid=user_id: update_account_status(uid, 0),
            )
            deactivate_button.place(x=540, y=60)

    clear_content()
    load_users()




def on_grades_click():
    clear_content()
    content_label = ctk.CTkLabel(content_frame, text="Gestion des notes", font=("Helvetica", 16))
    content_label.place(relx=0.5, rely=0.5, anchor="center")





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
title_label.place(x=76, y=170)

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
student_button = ctk.CTkButton(menu_frame, text="Profs Management", command=display_teachers, font=("Helvetica", 14, "bold"), width=200, anchor="w",height=40, corner_radius= 10,fg_color= "transparent",text_color="white",image=bg_img_user,compound=tkinter.LEFT)
student_button.place(x=65, y=370)
course_button = ctk.CTkButton(menu_frame, text="Voice Assitant", command=on_course_click, **button_style,image=bg_img_book,compound=tkinter.LEFT)
course_button.place(x=65, y=430)    # Position (x=35, y=250)
 # Position (x=35, y=310)

# schedule_button = ctk.CTkButton(menu_frame, text="Emploi du temps", command=validation, **button_style,image=bg_img_time,compound=tkinter.LEFT)
# schedule_button.place(x=65, y=470)# Position (x=35, y=370)

schedule_button = ctk.CTkButton(menu_frame, text="Validation des comptes", command=validation, **button_style,image=bg_img_time,compound=tkinter.LEFT)
schedule_button.place(x=65, y=250)


grades_button = ctk.CTkButton(menu_frame, text="Student Management", command=display_students, **button_style,image=bg_img_notes,compound=tkinter.LEFT)
grades_button.place(x=65, y=310)# Position (x=35, y=430)

  # Position (x=35, y=490)


settings_button = ctk.CTkButton(menu_frame,text="log out", command=on_settings_click, **logout_button_style,image=bg_img_logout,compound=tkinter.LEFT)
settings_button.place(x=65, y=550)  # Position (x=35, y=610)

# Cadre pour le contenu (à droite)
content_frame = ctk.CTkFrame(root, width=720, height=600, fg_color="#F0F0F0", corner_radius=0)
content_frame.place(x=282, y=0)  # Position fixe à droite

# Lancement de l'application
root.mainloop()
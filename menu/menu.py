import sqlite3
import tkinter
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def on_student_click():
    clear_content()
    content_label = ctk.CTkLabel(content_frame, text="Gestion des étudiants", font=("Helvetica", 16))
    content_label.place(relx=0.5, rely=0.5, anchor="center")

def on_course_click():
    clear_content()
    content_label = ctk.CTkLabel(content_frame, text="Gestion des cours", font=("Helvetica", 16))
    content_label.place(relx=0.5, rely=0.5, anchor="center")

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
student_button = ctk.CTkButton(menu_frame, text="Presence", command=on_student_click, font=("Helvetica", 14, "bold"), width=200, anchor="w",height=40, corner_radius= 10,fg_color= "transparent",text_color="white",image=bg_img_user,compound=tkinter.LEFT)
student_button.place(x=65, y=370)
course_button = ctk.CTkButton(menu_frame, text="Voice Assitant", command=on_course_click, **button_style,image=bg_img_book,compound=tkinter.LEFT)
course_button.place(x=65, y=310)   # Position (x=35, y=250)
 # Position (x=35, y=310)

schedule_button = ctk.CTkButton(menu_frame, text="Emploi du temps", command=on_schedule_click, **button_style,image=bg_img_time,compound=tkinter.LEFT)
schedule_button.place(x=65, y=250) # Position (x=35, y=370)

grades_button = ctk.CTkButton(menu_frame, text="Notes", command=on_grades_click, **button_style,image=bg_img_notes,compound=tkinter.LEFT)
grades_button.place(x=65, y=430)# Position (x=35, y=430)

  # Position (x=35, y=490)


settings_button = ctk.CTkButton(menu_frame,text="log out", command=on_settings_click, **logout_button_style,image=bg_img_logout,compound=tkinter.LEFT)
settings_button.place(x=65, y=550)  # Position (x=35, y=610)

# Cadre pour le contenu (à droite)
content_frame = ctk.CTkFrame(root, width=720, height=600, fg_color="#F0F0F0", corner_radius=0)
content_frame.place(x=282, y=0)  # Position fixe à droite


root.mainloop()
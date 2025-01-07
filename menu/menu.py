import tkinter

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

def on_schedule_click():
    clear_content()
    content_label = ctk.CTkLabel(content_frame, text="Gestion de l'emploi du temps", font=("Helvetica", 16))
    content_label.place(relx=0.5, rely=0.5, anchor="center")

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

# Lancement de l'application
root.mainloop()
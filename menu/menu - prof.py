import sqlite3
import tkinter
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
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
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT module_name FROM modules WHERE semester = ?', (semester,))
    modules = cursor.fetchall()
    conn.close()
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

                conn = sqlite3.connect('users.db')
                cursor = conn.cursor()
                cursor.execute(''' 
                    INSERT INTO notes (iduser, idmodule, note) 
                    VALUES (?, ?, ?)
                ''', (user_id, module_id, grade))
                conn.commit()
                conn.close()


    save_button = ctk.CTkButton(
        content_frame, text="Save Grades", command=on_save_grades, fg_color="#4CAF50", hover_color="#45a049"
    )
    save_button.grid(row=1,column=0)
def get_users_by_module(semester, module_name):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Fetch the id of the module
    cursor.execute('''
       SELECT id
       FROM modules
       WHERE module_name = ?
    ''', (module_name,))
    module_data = cursor.fetchone()

    if module_data is None:
        print(f"No module found with the name '{module_name}'.")
        conn.close()
        return []

    module_id = module_data[0]  # Extract the module id

    # Fetch users by semester
    cursor.execute('''
       SELECT id, username, email
       FROM users
       WHERE level = ?
    ''', (semester,))
    users = cursor.fetchall()
    conn.close()

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
        conn.close()

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



student_button = ctk.CTkButton(menu_frame, text="Presence", command=on_student_click, font=("Helvetica", 14, "bold"), width=200, anchor="w",height=40, corner_radius= 10,fg_color= "transparent",text_color="white",image=bg_img_user,compound=tkinter.LEFT)
student_button.place(x=65, y=370)
course_button = ctk.CTkButton(menu_frame, text="Voice Assitant", command=on_course_click, **button_style,image=bg_img_book,compound=tkinter.LEFT)
course_button.place(x=65, y=310)


schedule_button = ctk.CTkButton(menu_frame, text="Emploi du temps", command=on_schedule_click, **button_style,image=bg_img_time,compound=tkinter.LEFT)
schedule_button.place(x=65, y=250)

grades_button = ctk.CTkButton(menu_frame, text="Notes", command=on_grades_click, **button_style,image=bg_img_notes,compound=tkinter.LEFT)
grades_button.place(x=65, y=430)




settings_button = ctk.CTkButton(menu_frame,text="log out", command=on_settings_click, **logout_button_style,image=bg_img_logout,compound=tkinter.LEFT)
settings_button.place(x=65, y=550)


content_frame = ctk.CTkFrame(root, width=720, height=600, fg_color="#F0F0F0", corner_radius=0)
content_frame.place(x=282, y=0)




root.mainloop()
from customtkinter import *
from PIL import Image

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

# Create CTkFrame
frame1 = CTkFrame(
    main,
    fg_color="#33aef4",
    bg_color="white",
    corner_radius=40
)
frame1.place(relx=0.52, rely=0, relwidth=0.6, relheight=1)
#
#
# bg_label = CTkLabel(frame1, image=bg_imgg, text="")
# bg_label.place(relx=0, rely=-0.02, relwidth=1, relheight=1)


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
    width=50
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

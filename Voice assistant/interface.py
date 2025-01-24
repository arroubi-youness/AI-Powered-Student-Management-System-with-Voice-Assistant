import asyncio
import threading

from PIL import Image
from customtkinter import *
import azuregpt4

voice_assistant= azuregpt4.Voice_Assistant()
def call_handle_send():
    threading.Thread(target=handle_send,daemon=True).start()

def handle_send():
    user_message = user_input.get()

    display_message("You", user_message)
    assistant_response = voice_assistant.ask_assistant(user_message)

    # threading.Thread(target=voice_assistant.text_to_speech_fnc, args=(assistant_response,)).start()
    display_message("assistant", assistant_response)

    user_input.delete(0, END)



def display_message( sender, message):
        """Display a message in the chat display."""
        chat_display.configure(state="normal")
        chat_display.insert(END, f"{sender}: {message}\n")
        chat_display.configure(state="disabled")
        chat_display.see(END)

chat_interface=CTk()

chat_interface.title("voice assistant")
chat_interface.geometry("600x500")
chat_interface._set_appearance_mode("light")

chat_interface.resizable(False,False)

chat_display=CTkTextbox(chat_interface,width=550,height=350,state="disabled",wrap="word")
chat_display.grid(row=0,column=0,columnspan=3,padx=20,pady=10,sticky="nsew")

user_input = CTkEntry(chat_interface, placeholder_text="Type your message here...")
user_input.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

send_button = CTkButton(chat_interface, text="Send", command=call_handle_send)
send_button.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

voice_img = CTkImage(dark_image=Image.open("ressources/sound-wave.png"), size=(30,20))


voice_button = CTkButton(chat_interface, image=voice_img,text="",bg_color="white",corner_radius=200, command=voice_assistant.call_voice_assistant,width=30,height=20)
voice_button.grid(row=1, column=2, padx=(10,20), pady=10, sticky="ew")

chat_interface.mainloop()


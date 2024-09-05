import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import model3d_pages
import stream_home_page
import socket


def get_ip_address():
    try:
        # Connessione a un server esterno per determinare l'IP locale
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))  # Connessione a un server DNS pubblico
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Errore: {e}"

# Funzione per chiudere l'applicazione
def chiudi_applicazione():
    root.destroy()

# Creazione della finestra principale
global gif_frames, gif_frames_r, scale_bool

scale_bool = False
sott_elem= 150

root = tk.Tk()
root.title("HoloOS")
root.config(cursor="dot white")

# Ottieni le dimensioni dello schermo
larghezza_schermo = root.winfo_screenwidth()
altezza_schermo = root.winfo_screenheight()

# Imposta la dimensione massima della finestra
root.geometry(f"{larghezza_schermo}x{altezza_schermo}")
root.configure(background='black')

frame = tk.Frame(root)
frame.pack()

canvas = tk.Canvas(frame, bg="black", width=larghezza_schermo, height=altezza_schermo)
canvas.pack()

# Mantieni i riferimenti alle immagini
canvas.images = {}

# Center Button
original_center = Image.open("./assets/center.png")
center = ImageTk.PhotoImage(original_center)
canvas.images['center'] = center

# Game
original_game = Image.open("./assets/controller.png")
game = ImageTk.PhotoImage(original_game)
canvas.images['game'] = game

# Setting
original_setting = Image.open("./assets/settings.png")
setting = ImageTk.PhotoImage(original_setting)
canvas.images['setting'] = setting

# Airplay
original_airplay = Image.open("./assets/airplay.png")
airplay = ImageTk.PhotoImage(original_airplay)
canvas.images['airplay'] = airplay

# 3dmodel
original_3dmodel = Image.open("./assets/3dbox.png")
model = ImageTk.PhotoImage(original_3dmodel)
canvas.images['model'] = model

# Center Back
original_image = Image.open("./assets/background.png")  # Center Back
resized_image = original_image.resize((1100, 820), Image.BICUBIC)
photoimage = ImageTk.PhotoImage(resized_image)
canvas.images['photoimage'] = photoimage

def scale_center(event, element):
    original_scale_center = Image.open("./assets/center.png")
    resized_scale_center = original_scale_center.resize((250, 250), Image.BICUBIC)
    scale_center = ImageTk.PhotoImage(resized_scale_center)
    canvas.itemconfig(element, image=scale_center)
    canvas.images['scale_center'] = scale_center  # Mantieni un riferimento
    
def descale_center(event, element):
    canvas.itemconfig(element, image=canvas.images['center'])
    
def ai_scale_center(event):
    global scale_bool
    scale_bool = True

def ai_descale_center(event):
    global scale_bool
    scale_bool = False
    
def button_click(event, element):
    if element == game_icone:
        print("game click")
    elif element == setting_icone:
        print("settings click")
    elif element == airplay_icone:
        print("MIRRORRING click")
        stream_home_page.stream_homepage(root)
    elif element == model_icone:
        print("3dmodel click")
        model3d_pages.model3d_page_home(root)

def mostra_frame(frame_index):
    global gif_frames, gif_frames_r, scale_bool
    if scale_bool:
        canvas.itemconfig(gif_display, image=gif_frames_r[frame_index])
        root.after(60, lambda: mostra_frame((frame_index + 1) % len(gif_frames_r)))
    else:
        canvas.itemconfig(gif_display, image=gif_frames[frame_index])
        root.after(60, lambda: mostra_frame((frame_index + 1) % len(gif_frames)))        

ip_address = get_ip_address()
canvas.create_text(larghezza_schermo / 2, 50, text=ip_address, font=("Arial", 28), fill="white")

gif_path = "./assets/AI-animation.gif"
gif = Image.open(gif_path)
gif_frames = [frame.convert("RGBA") for frame in ImageSequence.Iterator(gif)]
gif_frames = [ImageTk.PhotoImage(frame) for frame in gif_frames]
canvas.images['gif_frames'] = gif_frames

gif_r = Image.open(gif_path)
gif_frames_r = [frame.convert("RGBA") for frame in ImageSequence.Iterator(gif_r)]
gif_frames_r = [frame.resize((500, 500), Image.BICUBIC) for frame in gif_frames_r]
gif_frames_r = [ImageTk.PhotoImage(frame) for frame in gif_frames_r]
canvas.images['gif_frames_r'] = gif_frames_r

canvas.create_image(larghezza_schermo / 2, altezza_schermo / 2 +sott_elem, image=photoimage)

game_center = canvas.create_image(250, 150+sott_elem, image=center)
game_icone = canvas.create_image(250, 150+sott_elem, image=game)
canvas.tag_bind(game_icone, "<Enter>", lambda event, element=game_center: scale_center(event, element))
canvas.tag_bind(game_icone, "<Leave>", lambda event, element=game_center: descale_center(event, element))
canvas.tag_bind(game_icone, "<Button-1>", lambda event, element=game_icone: button_click(event, element))

setting_center = canvas.create_image(250, altezza_schermo - 250 - 30+sott_elem, image=center)
setting_icone = canvas.create_image(250, altezza_schermo - 250 - 30+sott_elem, image=setting)
canvas.tag_bind(setting_icone, "<Enter>", lambda event, element=setting_center: scale_center(event, element))
canvas.tag_bind(setting_icone, "<Leave>", lambda event, element=setting_center: descale_center(event, element))
canvas.tag_bind(setting_icone, "<Button-1>", lambda event, element=setting_icone: button_click(event, element))

airplay_center = canvas.create_image(larghezza_schermo - 250 - 60, 150+sott_elem, image=center)
airplay_icone = canvas.create_image(larghezza_schermo - 250 - 60, 150+sott_elem, image=airplay)
canvas.tag_bind(airplay_icone, "<Enter>", lambda event, element=airplay_center: scale_center(event, element))
canvas.tag_bind(airplay_icone, "<Leave>", lambda event, element=airplay_center: descale_center(event, element))
canvas.tag_bind(airplay_icone, "<Button-1>", lambda event, element=airplay_icone: button_click(event, element))

model_center = canvas.create_image(larghezza_schermo - 250 - 60, altezza_schermo - 250 - 30+sott_elem, image=center)
model_icone = canvas.create_image(larghezza_schermo - 250 - 60, altezza_schermo - 250 - 30+sott_elem, image=model)
canvas.tag_bind(model_icone, "<Enter>", lambda event, element=model_center: scale_center(event, element))
canvas.tag_bind(model_icone, "<Leave>", lambda event, element=model_center: descale_center(event, element))
canvas.tag_bind(model_icone, "<Button-1>", lambda event, element=model_icone: button_click(event, element))

gif_display = canvas.create_image(larghezza_schermo / 2, altezza_schermo / 2 - 35+sott_elem, image=gif_frames[0])
canvas.tag_bind(gif_display, "<Enter>", lambda event: ai_scale_center(event))
canvas.tag_bind(gif_display, "<Leave>", lambda event: ai_descale_center(event))
mostra_frame(1)

root.mainloop()

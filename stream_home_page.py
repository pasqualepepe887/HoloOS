import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
from file_dialog import FileDialog
import subprocess
import multiprocessing

global url_path

def update_url_path(second_window,url_entry):
    global url_path
    if url_entry.get() :
        url_path=url_entry.get()
       
        
    
    second_window.after(2000, update_url_path,second_window,url_entry)

def return_page(root,back_page,attual_page):

    attual_page.destroy()
    if (back_page =="ANDROID_PAGE"):
        print("ANDROID_PAGE")
        streamANDROID(root)
    elif (back_page =="IOS_PAGE"):
        streamIOS(root)



def streamIOS(initial_window):
    global url_path
    
    subprocess.run(['python3', 'streamIOS.py', url_path])

def streamANDROID(initial_window):
    global url_path
    subprocess.run(['vlc', url_path])


def generate_from_image_selected(new_path,initial_window):
    initial_window.destroy()
    subprocess.run(['python3', 'generate_from_image_system.py', new_path])


# Funzione per caricare le immagini dopo aver creato la finestra principale
def load_images():
    global canvas_images
    canvas_images = {}

    original_center_model3dpage = Image.open("./assets/center.png")
    center_model3dpage = ImageTk.PhotoImage(original_center_model3dpage)
    canvas_images['center_model3dpage'] = center_model3dpage

    original_ios = Image.open("./assets/mirroring/ios.png")
    ios = ImageTk.PhotoImage(original_ios)
    canvas_images['ios'] = ios

    original_backForeward = Image.open("./assets/model3dpage/icone/backForeward.png")
    backForeward = ImageTk.PhotoImage(original_backForeward)
    canvas_images['backForeward'] = backForeward
    
    original_android = Image.open("./assets/mirroring/android.png")
    android = ImageTk.PhotoImage(original_android)
    canvas_images['android'] = android
    

def scale_center(event, element,canvas):
    original_scale_center = Image.open("./assets/center.png")
    resized_scale_center = original_scale_center.resize((250, 250), Image.BICUBIC)
    scale_center_image = ImageTk.PhotoImage(resized_scale_center)
    canvas.itemconfig(element, image=scale_center_image)
    canvas_images['scale_center'] = scale_center_image
    
def descale_center(event, element,canvas):
    canvas.itemconfig(element, image=canvas_images['center_model3dpage'])


def stream_homepage(root):
    second_window = tk.Toplevel(root)
    second_window.title("Stream")
    second_window.config(cursor="dot white")
    second_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    second_window.configure(background='black')
    second_window.attributes('-fullscreen', False) #TRUE
    second_window.attributes('-topmost', True)

    frame = tk.Frame(second_window)
    frame.pack()

    canvas = tk.Canvas(frame, bg="black", width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas.pack()
    

    font_family = "Nasalization"
# Carica il font .otf utilizzando il nome installato nel sistema
    custom_font = font.Font(family=font_family, size=24)
# Scrivi del testo sul canvas con il font personalizzato
    canvas.create_text(500, 450, text="ANDROID", font=custom_font, fill="white")

    
    canvas.create_text(900, 450, text="IOS", font=custom_font, fill="white")
    
    canvas.create_text(700, 550, text="URL", font=custom_font, fill="white")
    url_text = tk.Entry(second_window,bg="black", fg="white",font=custom_font)
    url_text_window = canvas.create_window(700, 600, window=url_text, width=550)
    update_url_path(second_window,url_text)
    
    load_images()

    backForeward_center = canvas.create_image(150, 130, image=canvas_images['center_model3dpage'])  # backForeward C
    backForeward_icone = canvas.create_image(150, 130, image=canvas_images['backForeward'])  # backForeward I
    canvas.tag_bind(backForeward_icone, "<Enter>", lambda event, element=backForeward_center, canvas=canvas: scale_center(event, element,canvas))
    canvas.tag_bind(backForeward_icone, "<Leave>", lambda event, element=backForeward_center, canvas=canvas: descale_center(event, element,canvas))
    canvas.tag_bind(backForeward_icone, "<Button-1>", lambda event: second_window.destroy())
    
    android_center = canvas.create_image(500, 300, image=canvas_images['center_model3dpage'])  # android C
    android_icone = canvas.create_image(500, 300, image=canvas_images['android'])  # android I
    canvas.tag_bind(android_icone, "<Enter>", lambda event, element=android_center, canvas=canvas: scale_center(event, element,canvas))
    canvas.tag_bind(android_icone, "<Leave>", lambda event, element=android_center,canvas=canvas: descale_center(event, element,canvas))
    canvas.tag_bind(android_icone, "<Button-1>", lambda event, root_page=root,backpage="ANDROID_PAGE", actual_page=second_window: return_page(root_page,backpage,actual_page))
    
    ios_center = canvas.create_image(900, 300, image=canvas_images['center_model3dpage'])  # ios C
    ios_icone = canvas.create_image(900, 300, image=canvas_images['ios'])  # ios I
    canvas.tag_bind(ios_icone, "<Enter>", lambda event, element=ios_center, canvas=canvas: scale_center(event, element,canvas))
    canvas.tag_bind(ios_icone, "<Leave>", lambda event, element=ios_center,canvas=canvas: descale_center(event, element,canvas))
    canvas.tag_bind(ios_icone, "<Button-1>", lambda event, root_page=root, backpage="IOS_PAGE", actual_page=second_window: return_page(root_page, backpage, actual_page))
    

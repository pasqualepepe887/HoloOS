import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from tkinter import font
import subprocess
from tkinter import messagebox
import time
import re

from supabase import create_client, Client

url = "https://avvwjxcemgfdjcoqxzoe.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF2dndqeGNlbWdmZGpjb3F4em9lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjQ3NDYwMDMsImV4cCI6MjA0MDMyMjAwM30.l14tI1XAZ_j8BPFSgamnXMItI2CFzWilUEPKBosogAM"
supabase: Client = create_client(url, key)


global psswd_selcted
global email

def close_config(root):

    data = {
    'email': email,
     }

    response = supabase.table('emails').insert(data).execute()

    root.destroy()

    content = 'Config'
    with open("config.txt", 'w') as file:
    # Scrivi il contenuto nel file
           file.write(content)

    subprocess.run(['python3', 'main.py'])
    
def scale_center(event, element):
    original_scale_center = Image.open("./assets/center.png")
    resized_scale_center = original_scale_center.resize((250, 250), Image.BICUBIC)
    scale_center = ImageTk.PhotoImage(resized_scale_center)
    canvas.itemconfig(element, image=scale_center)
    canvas.images['scale_center'] = scale_center  # Mantieni un riferimento
    
def descale_center(event, element):
    canvas.itemconfig(element, image=canvas.images['center'])

def update_psswd(second_window,psswd_entry):
    global psswd_selcted
    if psswd_entry.get() :
        psswd_selcted=psswd_entry.get()
       
    second_window.after(1000, update_psswd,second_window,psswd_entry)

def update_email(second_window,email_entry):
    global email
    if email_entry.get() :
       email=email_entry.get()
       
    second_window.after(1000, update_email,second_window,email_entry)

def get_email():
        canvas.delete("all")
        canvas.create_text(larghezza_schermo/2-30, 220, text="For future Updates", font=custom_font, fill="white")
        canvas.create_text(larghezza_schermo/2-30, 300, text="Your Email", font=custom_font_info, fill="white")
        email_text = tk.Entry(root,bg="black", fg="white",font=custom_font_info)
        email_text_window = canvas.create_window(600, 400, window=email_text, width=400,height=80)
        update_email(root,email_text)
        
        
        next_center = canvas.create_image(larghezza_schermo/2-30, altezza_schermo/2+200, image=center)
        next_button = canvas.create_text(larghezza_schermo/2-30, altezza_schermo/2+200, text="NEXT", font=custom_font_button, fill="white")
        canvas.tag_bind(next_button, "<Enter>", lambda event, element=next_center: scale_center(event, element))
        canvas.tag_bind(next_button, "<Leave>", lambda event, element=next_center: descale_center(event, element))
        canvas.tag_bind(next_button, "<Button-1>", lambda event,window=root: close_config(window))
        
def remove_specific_word(s, word_to_remove):
    """
    Rimuove una parola specifica se appare alla fine della stringa.
    """
    parts = s.split()
    # Controlla se l'ultima parola è quella che vogliamo rimuovere
    if parts and parts[-1] == word_to_remove:
        return " ".join(parts[:-1])  # Restituisci la stringa senza l'ultima parola
    return s

def get_wifi_list():
    """
    Esegue il comando nmcli per ottenere la lista delle reti Wi-Fi disponibili e
    rimuove la parola specifica "Infra" se appare alla fine di ogni SSID.
    """
    result = subprocess.run(['sudo','nmcli', 'dev', 'wifi'], capture_output=True, text=True)
    wifi_list = result.stdout.splitlines()[1:] 
    networks = []
    
    # Iteriamo attraverso le prime 5 reti Wi-Fi (o meno se non ce ne sono abbastanza)
    for line in wifi_list[:5]:
        parts = line.split()
        # Costruisci l'SSID unendo le parti da index 1 fino a prima di index -7
        ssid = " ".join(parts[1:-7])
        # Rimuovi la parola specifica "Infra" se appare alla fine
        clean_ssid = remove_specific_word(ssid, "Infra")
        networks.append(clean_ssid)
    
    return networks
def connect_to_wifi(ssid):
  
    global psswd_selcted
    # Comando per connettersi alla rete Wi-Fi selezionata
    result = subprocess.run(['sudo','nmcli', 'dev', 'wifi', 'connect', ssid, 'password',psswd_selcted],
                            capture_output=True, text=True)

    if result.returncode == 0:
        #messagebox.showinfo("Successo", f"Connesso a {ssid}")
        canvas.delete("all")
        canvas.create_text(larghezza_schermo/2-30, altezza_schermo/2-10, text="Connected", font=custom_font, fill="white")
        root.after(2500, get_email)

        
    else:
        messagebox.showerror("Errore", f"Connessione a {ssid} fallita.\n{result.stderr}")



def wifi_config_psswd(root,ssid):
     global psswd_selcted
     canvas.delete("all")
    
     canvas.create_text(larghezza_schermo/2-30, 220, text="Password", font=custom_font, fill="white")
 
     psswd_text = tk.Entry(root,bg="black", fg="white",font=custom_font_info,show='*')
     psswd_text_window = canvas.create_window(600, 350, window=psswd_text, width=400,height=80)
     update_psswd(root,psswd_text)
 
 
 
     next_center = canvas.create_image(larghezza_schermo/2+100, altezza_schermo/2+230, image=center)
     next_button = canvas.create_text(larghezza_schermo/2+100, altezza_schermo/2+230, text="NEXT", font=custom_font_button, fill="white")
     canvas.tag_bind(next_button, "<Enter>", lambda event, element=next_center: scale_center(event, element))
     canvas.tag_bind(next_button, "<Leave>", lambda event, element=next_center: descale_center(event, element))
     canvas.tag_bind(next_button, "<Button-1>", lambda event, wifi_name=ssid: connect_to_wifi(wifi_name))
     
     backForeward_center = canvas.create_image(larghezza_schermo/2-150,  altezza_schermo/2+230, image=center)  # backForeward C
     backForeward_icone = canvas.create_image(larghezza_schermo/2-150,  altezza_schermo/2+230, image=backForeward)  # backForeward I
     canvas.tag_bind(backForeward_icone, "<Enter>", lambda event, element=backForeward_center: scale_center(event, element))
     canvas.tag_bind(backForeward_icone, "<Leave>", lambda event, element=backForeward_center: descale_center(event, element))
     canvas.tag_bind(backForeward_icone, "<Button-1>", lambda event,window=root: wifi_config_ssid(window))

def wifi_config_ssid(root):
    canvas.delete("all")
    
    canvas.create_text(larghezza_schermo/2-30, 200, text="Choose a WiFi", font=custom_font, fill="white")
    
    selected_wifi = tk.StringVar(value="")
    
    wifi_list = get_wifi_list()
    ind_alt = 0
    column_padding = 10  # Padding tra le colonne
    
    for wifi in wifi_list:
        ind_alt += 70
        
        # Creazione di un rettangolo per dare l'effetto di tabella
        rect_y0 = 205 + ind_alt 
        rect_y1 = 205 + ind_alt + 40
        canvas.create_rectangle(larghezza_schermo/2-400, rect_y0, larghezza_schermo/2+300, rect_y1, outline="white")
        
        # Creazione del testo per l'SSID del Wi-Fi
        wifi_label = canvas.create_text(larghezza_schermo/2-30, 220 + ind_alt, text=wifi, font=custom_font_info, fill="white")
        
        # Binding per il click del mouse
        canvas.tag_bind(wifi_label, "<Button-1>", lambda event, element=wifi_label,window=root: wifi_config_psswd(root,canvas.itemcget(element, "text")))
        canvas.tag_bind(wifi_label, "<Enter>", lambda event, element=wifi_label:  canvas.itemconfig(element, fill="gray"))
        canvas.tag_bind(wifi_label, "<Leave>", lambda event, element=wifi_label: canvas.itemconfig(element, fill="white"))
        
    backForeward_center = canvas.create_image(larghezza_schermo-170,  altezza_schermo-200, image=center)  # reload C
    backForeward_icone = canvas.create_image(larghezza_schermo-170,  altezza_schermo-200, image=reload)  # reload I
    canvas.tag_bind(backForeward_icone, "<Enter>", lambda event, element=backForeward_center: scale_center(event, element))
    canvas.tag_bind(backForeward_icone, "<Leave>", lambda event, element=backForeward_center: descale_center(event, element))
    canvas.tag_bind(backForeward_icone, "<Button-1>", lambda event,window=root: wifi_config_ssid(window))   


root = tk.Tk()
root.title("HoloOS-Config")
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

# Mantieni i riferimenti alle immagini
canvas.images = {}

# Center Button
original_center = Image.open("./assets/center.png")
center = ImageTk.PhotoImage(original_center)
canvas.images['center'] = center

original_backForeward = Image.open("./assets/backForeward.png")    
backForeward = ImageTk.PhotoImage(original_backForeward)
canvas.images['backForeward'] = backForeward

original_reload = Image.open("./assets/reload.png")    
reload = ImageTk.PhotoImage(original_reload)
canvas.images['reload'] = reload


font_family = "Nasalization"
# Carica il font .otf utilizzando il nome installato nel sistema
custom_font = font.Font(family=font_family, size=50)
custom_font_button = font.Font(family=font_family, size=28)
custom_font_info = font.Font(family=font_family, size=26)

canvas.create_text(larghezza_schermo/2-30, altezza_schermo/2-50, text="Holo-Project", font=custom_font, fill="white")
canvas.create_text(larghezza_schermo/2-30, altezza_schermo/2, text="By Pasquale Pepe", font=custom_font_info, fill="white")

next_center = canvas.create_image(larghezza_schermo/2-30, altezza_schermo/2+200, image=center)
next_button = canvas.create_text(larghezza_schermo/2-30, altezza_schermo/2+200, text="NEXT", font=custom_font_button, fill="white")
canvas.tag_bind(next_button, "<Enter>", lambda event, element=next_center: scale_center(event, element))
canvas.tag_bind(next_button, "<Leave>", lambda event, element=next_center: descale_center(event, element))
canvas.tag_bind(next_button, "<Button-1>", lambda event, element=next_button,window=root: wifi_config_ssid(window))

canvas.pack()

root.mainloop()



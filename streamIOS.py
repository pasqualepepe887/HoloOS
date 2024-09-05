import requests
import tkinter as tk
from PIL import Image, ImageTk
import io
import sys
import time

base_url = sys.argv[1]

# Funzione per scaricare, ridimensionare e mostrare l'immagine
def get_and_show_image(url, label):
    try:
        # Effettua una richiesta GET all'URL fornito
        response = requests.get(url)
        if response.status_code == 200:
            # Leggi l'immagine dalla risposta
            image_data = io.BytesIO(response.content)
            image = Image.open(image_data)
            
            # Riduci le dimensioni dell'immagine 
            larghezza_originale, altezza_originale = image.size
            nuova_larghezza = int(larghezza_originale * 0.43)
            nuova_altezza = int(altezza_originale * 0.43)
            image = image.resize((nuova_larghezza, nuova_altezza), Image.NEAREST)
            
            # Converti l'immagine in un oggetto PhotoImage per Tkinter
            photo = ImageTk.PhotoImage(image)
            
            # Aggiorna l'immagine nella label
            label.config(image=photo)
            label.image = photo
        else:
            print("Errore:", response.status_code)
    except Exception as e:
        print("Errore durante il recupero e la visualizzazione dell'immagine:", str(e))
        print("ERRORE NELLA COMUNICAZIONE CONTROLLA L'URL")

        sys.exit()
        


if __name__ == "__main__":
    # Creazione della finestra Tkinter
    root = tk.Tk()
    root.title("Stream IOS")
    root.configure(bg='black')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    
    # Creazione della label per visualizzare l'immagine
    image_label = tk.Label(root)
    image_label.pack()

    # Gestione della chiusura della finestra
    def on_closing():
        print("Chiusura della finestra")
        root.destroy()
        sys.exit()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Funzione per aggiornare l'immagine ogni secondo
    def update_image():
        try:
            # Costruisci l'URL dell'immagine usando il timestamp corrente
            timestamp = int(time.time())
            image_url = f"{base_url}image1786857180{timestamp}.jpg"
            
            # Scarica e mostra l'immagine
            get_and_show_image(image_url, image_label)
            
            # Richiama questa funzione nuovamente dopo 1000 millisecondi (1 secondo)
            root.after(5, update_image)
        except KeyboardInterrupt:
            print("Interrotto dall'utente")
            root.destroy()
        except:
            print("ERRORE NELLA COMUNICAZIONE CONTROLLA L'URL")
            root.destroy()
    
    # Funzione per gestire la pressione del tasto "q"
    def on_key_press(event):
        if event.char == "q":
            print("Tasto 'q' premuto: Chiusura dell'applicazione")
            root.destroy()
            sys.exit()

    # Associa la funzione on_key_press alla pressione del tasto "q"
    root.bind("<Key>", on_key_press)
    
    # Avvia l'aggiornamento dell'immagine
    update_image()
    
    # Avvia il loop principale di Tkinter
    root.mainloop()



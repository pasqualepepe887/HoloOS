import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import model3d_pages
import stream_home_page
import socket
import pandas as pd
import os
from tkinter import font
from file_dialog import FileDialog


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
global gif_frames, gif_frames_r, scale_bool, game_icone, setting_icone, airplay_icone, model_icone, gif_display, edit_state,path_file

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

#Font  System
font_family = "Nasalization"
custom_font_info = font.Font(family=font_family, size=20)


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

# backforeward
original_back = Image.open("./assets/backForeward.png")
back = ImageTk.PhotoImage(original_back)
canvas.images['back'] = back

# Center Back
original_image = Image.open("./assets/background.png")  # Center Back
resized_image = original_image.resize((1100, 820), Image.BICUBIC)
photoimage = ImageTk.PhotoImage(resized_image)
canvas.images['photoimage'] = photoimage

#Error
original_error = Image.open("./assets/error.png")  
icone_error = ImageTk.PhotoImage(original_error)
canvas.images["error"] = icone_error

#Edit
original_edit = Image.open("./assets/edit.png")  
icone_edit = ImageTk.PhotoImage(original_edit)
canvas.images["edit"] = icone_edit

#Cancel
original_cancel = Image.open("./assets/cancel.png")  
icone_cancel = ImageTk.PhotoImage(original_cancel)
canvas.images["cancel"] = icone_cancel

#Add
original_add = Image.open("./assets/add.png")  
icone_add = ImageTk.PhotoImage(original_add)
canvas.images["add"] = icone_add

#Right Arrow
original_right_arrow = Image.open("./assets/right_arrow.png")  
right_arrow = ImageTk.PhotoImage(original_right_arrow)
canvas.images["right_arrow"] = right_arrow

#Home
original_home = Image.open("./assets/home.png")  
home_icon = ImageTk.PhotoImage(original_home)
canvas.images["home_icon"] = home_icon

#Left Arrow
original_left_arrow=original_right_arrow.transpose(Image.FLIP_LEFT_RIGHT)
left_arrow = ImageTk.PhotoImage(original_left_arrow)
canvas.images["left_arrow"] = left_arrow

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


def add_app_icone(icone_path,app_name):
    try:
         original_app = Image.open(icone_path)  
         icone_app = ImageTk.PhotoImage(original_app)
         canvas.images[app_name] = icone_app
    
         return icone_app
    except:
         return canvas.images["error"]
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

def edit_mode(number_page):
    global edit_state
    if edit_state== False:
        edit_state = True
        app_landing_page(number_page)
    else:
        edit_state = False
        app_landing_page(number_page)

def remove_app(app_number,total_app):
    df = pd.read_excel('app_storege.xlsx')
    df= df.drop(index=app_number)
    df.to_excel('app_storege.xlsx',index=False)
    app_landing_page(total_app)

def update_path(path):
    global path_file
    path_file=path

def add_app_storage(app_name_entry,command_entry,number_page):
    global path_file
    app_name=app_name_entry.get()
    command=command_entry.get()
    df = pd.read_excel('app_storege.xlsx')    
    new_app = pd.DataFrame([{'name_app':app_name,'Icone_path':path_file, 'bash_command':command}])

    df=pd.concat([df,new_app],ignore_index=True)
    df.to_excel('app_storege.xlsx',index=False)
    app_landing_page(number_page)



def select_path(file_button):
    
    path_file_selected = ""
    loadFile_window = tk.Toplevel(root)
   
    file_dialog = FileDialog(loadFile_window,".png", path_file_selected,on_export_path_change=lambda path: (file_button.insert(0,path),update_path(path),loadFile_window.destroy()) )
    file_dialog.pack( expand=False) 


def add_app(numbero_app_state):
    
    canvas.delete("all")

    canvas.create_text(larghezza_schermo/2-150, 200+sott_elem, text="App Name", font=custom_font_info, fill="white")
    app_name_entry = tk.Entry(root,bg="black", fg="white",font=custom_font_info)
    app_name__window = canvas.create_window(larghezza_schermo/2-30+150, 200+sott_elem, window= app_name_entry , width=300,height=50)

    canvas.create_text(larghezza_schermo/2-150, 300+sott_elem, text="Icon Path", font=custom_font_info, fill="white")
    
    file_button_entry = tk.Entry(root,bg="black", fg="white",font=custom_font_info)
    file_button_window = canvas.create_window(larghezza_schermo/2+120, 300+sott_elem , window= file_button_entry , width=300,height=50)

    
   # file_button = canvas.create_text(larghezza_schermo/2+150, 300 , text="SELECT", font=custom_font_info, fill="white")
    file_button_entry.bind("<Double-1>", lambda event, component= file_button_entry: select_path(component))



    canvas.create_text(larghezza_schermo/2-150, 400+sott_elem, text="Command", font=custom_font_info, fill="white")
    app_command_entry = tk.Entry(root,bg="black", fg="white",font=custom_font_info)
    app_command__window = canvas.create_window(larghezza_schermo/2-30+150, 400+sott_elem, window= app_command_entry , width=300,height=50)


    next_center = canvas.create_image(larghezza_schermo -200, altezza_schermo - 220 , image=center)
    next_button = canvas.create_text(larghezza_schermo -200, altezza_schermo - 220 , text="ADD", font=custom_font_info, fill="white")
    canvas.tag_bind(next_button, "<Enter>", lambda event, element=next_center: scale_center(event, element))
    canvas.tag_bind(next_button, "<Leave>", lambda event, element=next_center: descale_center(event, element))
    canvas.tag_bind(next_button, "<Button-1>", lambda event, app_name=app_name_entry,command=app_command_entry: add_app_storage(app_name,command,numbero_app_state))
    
    
    back_center = canvas.create_image(200 , altezza_schermo - 220 , image=center)
    back_icone = canvas.create_image(200, altezza_schermo - 220 , image=back)
    canvas.tag_bind(back_icone, "<Enter>", lambda event, element=back_center: scale_center(event, element))
    canvas.tag_bind(back_icone, "<Leave>", lambda event, element=back_center: descale_center(event, element))
    canvas.tag_bind(back_icone, "<Button-1>", lambda event, number=numbero_app_state: app_landing_page(number))  



def app_landing_page(numbero_app_state):
    global edit_state
    
    if edit_state == False:
    
        canvas.delete("all")
    
        df = pd.read_excel('app_storege.xlsx')
        numero_app = df.shape[0]  #numero di righe

        counter_app =0
        padding_app_lateral= 150
        padding_top_app =0
        max_appr_riga = 3
        for i in range(numbero_app_state,numero_app):
       
          if numbero_app_state >=5:
            preview_page_icone = canvas.create_image(200 , altezza_schermo /2 -100, image=left_arrow )
            canvas.tag_bind(preview_page_icone, "<Button-1>", lambda event, number=(int(numbero_app_state-5)): app_landing_page(number))
           
    
          if i-numbero_app_state <5:
            app_name = df.iloc[i, 0]  # Qui estraggo il nome dell'app
            app_icone_path= df.iloc[i, 1]  # Qui estraggo l'icona dell'app
            app_command= df.iloc[i, 2]  # Qui estraggo il comando dell'app
            
            #print(app_name,app_icone_path,app_command)
        
            counter_app=counter_app+1
            padding_app_lateral=padding_app_lateral+250
            
            if counter_app >  max_appr_riga:
                padding_top_app= padding_top_app+ 250
                padding_app_lateral=530
                counter_app= 0
                max_appr_riga=2
                
    
            app_center = canvas.create_image(padding_app_lateral, 150+padding_top_app+sott_elem, image=center)
            app_icone = canvas.create_image(padding_app_lateral, 150+padding_top_app+sott_elem, image=add_app_icone( app_icone_path,app_name))
            canvas.tag_bind(app_icone, "<Enter>", lambda event, element=app_center: scale_center(event, element))
            canvas.tag_bind(app_icone, "<Leave>", lambda event, element=app_center: descale_center(event, element))
            canvas.tag_bind(app_icone, "<Button-1>", lambda event, command=app_command:os.system(command))
         
          elif i-numbero_app_state >=4:
            next_page_icone = canvas.create_image(larghezza_schermo -200 , altezza_schermo /2 -100, image=right_arrow )
            canvas.tag_bind(next_page_icone, "<Button-1>", lambda event, number=(i-numbero_app_state): app_landing_page(number))
            break
        
 
        back_center = canvas.create_image(200 , altezza_schermo - 220 , image=center)
        back_icone = canvas.create_image(200, altezza_schermo - 220 , image=home_icon)
        canvas.tag_bind(back_icone, "<Enter>", lambda event, element=back_center: scale_center(event, element))
        canvas.tag_bind(back_icone, "<Leave>", lambda event, element=back_center: descale_center(event, element))
        canvas.tag_bind(back_icone, "<Button-1>", lambda event: home_page())
    
    
        edit_center = canvas.create_image(larghezza_schermo -200, altezza_schermo - 220 , image=center)
        edit_icone = canvas.create_image(larghezza_schermo -200, altezza_schermo - 220 , image=icone_edit)
        canvas.tag_bind(edit_icone, "<Enter>", lambda event, element=edit_center: scale_center(event, element))
        canvas.tag_bind(edit_icone, "<Leave>", lambda event, element=edit_center: descale_center(event, element))
        canvas.tag_bind(edit_icone, "<Button-1>", lambda event: edit_mode(numbero_app_state))

    else:
        
        canvas.delete("all")
    
        df = pd.read_excel('app_storege.xlsx')
        numero_app = df.shape[0]  #numero di righe

        counter_app =0
        padding_app_lateral= 150
        padding_top_app =0
        max_appr_riga = 3
    
        for i in range(numbero_app_state,numero_app):
           
          if i-numbero_app_state <5:
            app_name = df.iloc[i, 0]  # Qui estraggo il nome dell'app
            app_icone_path= df.iloc[i, 1]  # Qui estraggo l'icona dell'app
            app_command= df.iloc[i, 2]  # Qui estraggo il comando dell'app
            
            #print(app_name,app_icone_path,app_command)
        
            counter_app=counter_app+1
            padding_app_lateral=padding_app_lateral+250
            
            if counter_app >  max_appr_riga:
                padding_top_app= padding_top_app+ 250
                padding_app_lateral=530
                counter_app= 0
                max_appr_riga=2
                
                
            app_center = canvas.create_image(padding_app_lateral, 150+padding_top_app+sott_elem, image=center)
            app_icone = canvas.create_image(padding_app_lateral, 150+padding_top_app+sott_elem, image=add_app_icone( app_icone_path,app_name))

            cancel_icone = canvas.create_image(padding_app_lateral+100, 100+padding_top_app-40+sott_elem , image=icone_cancel)
            canvas.tag_bind(cancel_icone, "<Button-1>", lambda event, app_number=i,total_app=numbero_app_state: remove_app(app_number,total_app))
          

        if numero_app-numbero_app_state <5:
            
             counter_app=counter_app+1
             padding_app_lateral=padding_app_lateral+250
            
             if counter_app >  3:
                padding_top_app= padding_top_app+ 250
                padding_app_lateral=530
                counter_app= 0
       
            
             add_center = canvas.create_image(padding_app_lateral, 150+padding_top_app+sott_elem , image=center)
             add_icone = canvas.create_image(padding_app_lateral, 150+padding_top_app+sott_elem, image=icone_add)
             canvas.tag_bind(add_icone, "<Enter>", lambda event, element=add_center: scale_center(event, element))
             canvas.tag_bind(add_icone, "<Leave>", lambda event, element=add_center: descale_center(event, element))
             canvas.tag_bind(add_icone, "<Button-1>", lambda event,total_app=numbero_app_state: add_app(total_app))

    
        back_center = canvas.create_image(200 , altezza_schermo - 220 , image=center)
        back_icone = canvas.create_image(200, altezza_schermo - 220 , image=home_icon)
        canvas.tag_bind(back_icone, "<Enter>", lambda event, element=back_center: scale_center(event, element))
        canvas.tag_bind(back_icone, "<Leave>", lambda event, element=back_center: descale_center(event, element))
        canvas.tag_bind(back_icone, "<Button-1>", lambda event: home_page())
    
    
        edit_center = canvas.create_image(larghezza_schermo -200, altezza_schermo - 220 , image=center)
        edit_icone = canvas.create_image(larghezza_schermo -200, altezza_schermo - 220 , image=icone_edit)
        canvas.tag_bind(edit_icone, "<Enter>", lambda event, element=edit_center: scale_center(event, element))
        canvas.tag_bind(edit_icone, "<Leave>", lambda event, element=edit_center: descale_center(event, element))
        canvas.tag_bind(edit_icone, "<Button-1>", lambda event: edit_mode(numbero_app_state))


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
    elif element == gif_display:
        print("Center click")
        app_landing_page(0)
        
        
def mostra_frame(frame_index,gif_display):
    global gif_frames, gif_frames_r, scale_bool
    if scale_bool:
        canvas.itemconfig(gif_display, image=gif_frames_r[frame_index])
        root.after(60, lambda: mostra_frame((frame_index + 1) % len(gif_frames_r),gif_display))
    else:
        canvas.itemconfig(gif_display, image=gif_frames[frame_index])
        root.after(60, lambda: mostra_frame((frame_index + 1) % len(gif_frames),gif_display))        



def home_page():
         global game_icone, setting_icone, airplay_icone, model_icone, gif_display, edit_state, path_file_selected
         edit_state = False
         path_file_selected= ""
         canvas.delete("all")
         
         canvas.create_image(larghezza_schermo / 2, altezza_schermo / 2 +sott_elem, image=photoimage)
         ip_address = get_ip_address()
         canvas.create_text(larghezza_schermo / 2, 50, text=ip_address, font=("Arial", 28), fill="white")
         
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
         canvas.tag_bind(gif_display, "<Button-1>", lambda event, element=gif_display: button_click(event, element))
         mostra_frame(1,gif_display)


home_page()
root.mainloop()
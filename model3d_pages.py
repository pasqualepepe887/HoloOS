import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
from file_dialog import FileDialog
import subprocess
import multiprocessing


sott_elem= 120

def return_page(root,back_page,attual_page):
    attual_page.destroy()
    if (back_page =="GENERATE_IMAGE"):
        generate_from_image_page(root)
    elif (back_page =="IMPORT_FILE"):
        load_file_page(root)
    elif (back_page =="MODEL3D_HOME"):
        model3d_page_home(root)


def import_file_selected(new_path,initial_window):
    initial_window.destroy()
    subprocess.run(['python3', '3drender.py', new_path])

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

    original_imageIcone = Image.open("./assets/model3dpage/icone/imageIcone.png")
    imageIcone = ImageTk.PhotoImage(original_imageIcone)
    canvas_images['imageIcone'] = imageIcone

    original_backForeward = Image.open("./assets/model3dpage/icone/backForeward.png")
    backForeward = ImageTk.PhotoImage(original_backForeward)
    canvas_images['backForeward'] = backForeward
    
    original_fileFolder = Image.open("./assets/model3dpage/icone/fileFolder.png")
    fileFolder = ImageTk.PhotoImage(original_fileFolder)
    canvas_images['fileFolder'] = fileFolder
    
    original_cloud = Image.open("./assets/model3dpage/icone/cloud.png")
    cloud = ImageTk.PhotoImage(original_cloud)
    canvas_images['cloud'] = cloud

def scale_center(event, element,canvas):
    original_scale_center = Image.open("./assets/center.png")
    resized_scale_center = original_scale_center.resize((250, 250), Image.BICUBIC)
    scale_center_image = ImageTk.PhotoImage(resized_scale_center)
    canvas.itemconfig(element, image=scale_center_image)
    canvas_images['scale_center'] = scale_center_image
    
def descale_center(event, element,canvas):
    canvas.itemconfig(element, image=canvas_images['center_model3dpage'])

#Funzione che verrà richiamata da main.py
def model3d_page_home(root):
    second_window = tk.Toplevel(root)
    second_window.title("Model 3D")
    second_window.config(cursor="dot white")
    second_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    second_window.configure(background='black')
    second_window.attributes('-fullscreen', False) #TRUE
    second_window.attributes('-topmost', True)

    frame = tk.Frame(second_window)
    frame.pack()

    canvas_model3dpage = tk.Canvas(frame, bg="black", width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas_model3dpage.pack()
    
    load_images()

    backForeward_center = canvas_model3dpage.create_image(150, 130+sott_elem, image=canvas_images['center_model3dpage'])  # backForeward C
    backForeward_icone = canvas_model3dpage.create_image(150, 130+sott_elem, image=canvas_images['backForeward'])  # backForeward I
    canvas_model3dpage.tag_bind(backForeward_icone, "<Enter>", lambda event, element=backForeward_center, canvas=canvas_model3dpage: scale_center(event, element,canvas))
    canvas_model3dpage.tag_bind(backForeward_icone, "<Leave>", lambda event, element=backForeward_center, canvas=canvas_model3dpage: descale_center(event, element,canvas))
    canvas_model3dpage.tag_bind(backForeward_icone, "<Button-1>", lambda event: second_window.destroy())
    
    imageIcone_center = canvas_model3dpage.create_image(500, 300+sott_elem, image=canvas_images['center_model3dpage'])  # imageIcone C
    imageIcone_icone = canvas_model3dpage.create_image(500, 300+sott_elem, image=canvas_images['imageIcone'])  # imageIcone I
    canvas_model3dpage.tag_bind(imageIcone_icone, "<Enter>", lambda event, element=imageIcone_center, canvas=canvas_model3dpage: scale_center(event, element,canvas))
    canvas_model3dpage.tag_bind(imageIcone_icone, "<Leave>", lambda event, element=imageIcone_center,canvas=canvas_model3dpage: descale_center(event, element,canvas))
    canvas_model3dpage.tag_bind(imageIcone_icone, "<Button-1>", lambda event, root_page=root,backpage="GENERATE_IMAGE", actual_page=second_window: return_page(root_page,backpage,actual_page))
    
    fileFolder_center = canvas_model3dpage.create_image(900, 300+sott_elem, image=canvas_images['center_model3dpage'])  # fileFolder C
    fileFolder_icone = canvas_model3dpage.create_image(900, 300+sott_elem, image=canvas_images['fileFolder'])  # fileFolder I
    canvas_model3dpage.tag_bind(fileFolder_icone, "<Enter>", lambda event, element=fileFolder_center, canvas=canvas_model3dpage: scale_center(event, element,canvas))
    canvas_model3dpage.tag_bind(fileFolder_icone, "<Leave>", lambda event, element=fileFolder_center,canvas=canvas_model3dpage: descale_center(event, element,canvas))
    canvas_model3dpage.tag_bind(fileFolder_icone, "<Button-1>", lambda event, root_page=root,backpage="IMPORT_FILE", actual_page=second_window: return_page(root_page,backpage,actual_page))
    
    font_family = "Nasalization"
# Carica il font .otf utilizzando il nome installato nel sistema
    custom_font = font.Font(family=font_family, size=24)
# Scrivi del testo sul canvas con il font personalizzato
    canvas_model3dpage.create_text(500, 450+sott_elem, text="GENERATE FROM", font=custom_font, fill="white")
    canvas_model3dpage.create_text(500, 500+sott_elem, text="IMAGE", font=custom_font, fill="white")
    
    canvas_model3dpage.create_text(900, 450+sott_elem, text="IMPORT FILE", font=custom_font, fill="white")

    
def generate_from_image_page(root):

    generteImage_window = tk.Toplevel(root)
    generteImage_window.title("3D Model Viewer")
    generteImage_window.config(cursor="dot white")
    generteImage_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    generteImage_window.configure(background='black')
    generteImage_window.attributes('-fullscreen', False) #TRUE
    generteImage_window.attributes('-topmost', True)

    frame = tk.Frame(generteImage_window)
    frame.pack()

    canvas_model3dpage = tk.Canvas(frame, bg="black", width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas_model3dpage.pack()
    
    load_images()

    backForeward_center = canvas_model3dpage.create_image(150, 130+sott_elem, image=canvas_images['center_model3dpage'])  # backForeward C
    backForeward_icone = canvas_model3dpage.create_image(150, 130+sott_elem, image=canvas_images['backForeward'])  # backForeward I
    canvas_model3dpage.tag_bind(backForeward_icone, "<Enter>", lambda event, element=backForeward_center, canvas=canvas_model3dpage: scale_center(event, element,canvas))
    canvas_model3dpage.tag_bind(backForeward_icone, "<Leave>", lambda event, element=backForeward_center, canvas=canvas_model3dpage: descale_center(event, element,canvas))
    canvas_model3dpage.tag_bind(backForeward_icone, "<Button-1>",lambda event, root_page=root,backpage="MODEL3D_HOME", actual_page=generteImage_window: return_page(root_page,backpage,actual_page))
    
   
   
    imageIcone_icone = canvas_model3dpage.create_image(875, 130+sott_elem, image=canvas_images['imageIcone'])  # imageIcone I
   
    font_family = "Nasalization"

    custom_font = font.Font(family=font_family, size=24)

    canvas_model3dpage.create_text(650, 105+sott_elem, text="GENERATE FROM", font=custom_font, fill="white")
    canvas_model3dpage.create_text(650, 155+sott_elem, text="IMAGE", font=custom_font, fill="white")
   
    path_file_selected= ""
   
    file_dialog = FileDialog(canvas_model3dpage,".jpg",path_file_selected,on_export_path_change=lambda path: generate_from_image_selected(path,  generteImage_window))
    file_dialog.pack(fill="both", expand=True)

    canvas_model3dpage.create_text(370, 250+sott_elem, text="Select a file", font=(font.Font(family=font_family, size=22)), fill="white")  
    file_dialog_window=canvas_model3dpage.create_window((180,280+sott_elem), window=file_dialog, anchor="nw")
    
    canvas_model3dpage.create_text(900, 250+sott_elem, text="Upload from", font=(font.Font(family=font_family, size=22)), fill="white")
    canvas_model3dpage.create_text(900, 300+sott_elem, text="the App", font=(font.Font(family=font_family, size=22)), fill="white")
    
    cloud_center = canvas_model3dpage.create_image(900, 450+sott_elem, image=canvas_images['center_model3dpage'])  # cloud C
    cloud_icone = canvas_model3dpage.create_image(900, 450+sott_elem, image=canvas_images['cloud'])  # cloud I    


def load_file_page(root):

    loadFile_window = tk.Toplevel(root)
    loadFile_window.title("3D Model Viewer")
    loadFile_window.config(cursor="dot white")
    loadFile_window.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    loadFile_window.configure(background='black')
    loadFile_window.attributes('-fullscreen', False) #TRUE
    loadFile_window.attributes('-topmost', True)

    frame = tk.Frame(loadFile_window)
    frame.pack()

    canvas_model3dpage = tk.Canvas(frame, bg="black", width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    canvas_model3dpage.pack()
    
    load_images()

    backForeward_center = canvas_model3dpage.create_image(150, 130+sott_elem, image=canvas_images['center_model3dpage'])  # backForeward C
    backForeward_icone = canvas_model3dpage.create_image(150, 130+sott_elem, image=canvas_images['backForeward'])  # backForeward I
    canvas_model3dpage.tag_bind(backForeward_icone, "<Enter>", lambda event, element=backForeward_center, canvas=canvas_model3dpage: scale_center(event, element,canvas))
    canvas_model3dpage.tag_bind(backForeward_icone, "<Leave>", lambda event, element=backForeward_center, canvas=canvas_model3dpage: descale_center(event, element,canvas))
    canvas_model3dpage.tag_bind(backForeward_icone, "<Button-1>",lambda event, root_page=root,backpage="MODEL3D_HOME", actual_page=loadFile_window: return_page(root_page,backpage,actual_page))
    
   
   
    imageIcone_icone = canvas_model3dpage.create_image(875, 105+sott_elem, image=canvas_images['fileFolder'])  # FILEfOLDER I
   
    font_family = "Nasalization"

    custom_font = font.Font(family=font_family, size=24)

    canvas_model3dpage.create_text(650, 105+sott_elem, text="IMPORT FILE", font=custom_font, fill="white")

    path_file_selected= ""
    
    file_dialog = FileDialog(canvas_model3dpage,".obj",path_file_selected,on_export_path_change=lambda path: import_file_selected(path, loadFile_window))
    file_dialog.pack(fill="both", expand=True)

    canvas_model3dpage.create_text(370, 250+sott_elem, text="Select a file", font=(font.Font(family=font_family, size=22)), fill="white")  
    file_dialog_window=canvas_model3dpage.create_window((180,280+sott_elem), window=file_dialog, anchor="nw")
    
    canvas_model3dpage.create_text(900, 250+sott_elem, text="Upload from", font=(font.Font(family=font_family, size=22)), fill="white")
    canvas_model3dpage.create_text(900, 300+sott_elem, text="the App", font=(font.Font(family=font_family, size=22)), fill="white")
    
    cloud_center = canvas_model3dpage.create_image(900, 450+sott_elem, image=canvas_images['center_model3dpage'])  # cloud C
    cloud_icone = canvas_model3dpage.create_image(900, 450+sott_elem, image=canvas_images['cloud'])  # cloud I 5

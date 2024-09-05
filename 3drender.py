from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, DirectionalLight, AmbientLight, Vec4
from direct.task import Task
import sys
import os

path_model3d = sys.argv[1]

class MyApp(ShowBase):
    def __init__(self):
        # Chiama il costruttore di ShowBase
        ShowBase.__init__(self)
        
        # Specifica la modalità fullscreen e altre proprietà della finestra
        props = WindowProperties()
        props.setSize(1920, 1080)  # Imposta la dimensione della finestra se non in modalità fullscreen
        props.setFullscreen(True)   # Imposta la modalità fullscreen
        props.setTitle("3drender")  # Imposta il titolo della finestra
        self.win.requestProperties(props)
        
        # Imposta il colore di sfondo su nero
        self.win.setClearColor((0, 0, 0, 1))
        
        # Carica il modello in formato OBJ
        self.model = self.loader.loadModel(path_model3d)

        #self.model.setScale(0.5)
        self.scale_model()

        # Rimuovi tutte le luci
        self.render.clearLight()
        
        # Imposta la posizione del modello nella scena
        self.model.reparentTo(self.render)
        self.model.setPos(0, 10, 0)
        
        # Imposta l'angolo di rotazione lungo l'asse delle Y
        self.heading_angle = 0
        
        # Avvia la rotazione del modello lungo l'asse delle Y
        self.rotate_task = taskMgr.add(self.rotate_model, "rotate_model")
        
        # Aggiungi una luce ambientale
        alight = AmbientLight('alight')
        alight.setColor(Vec4(1, 1, 1, 1))  # Colore bianco pieno
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)
        
        # Registra i key binding
        self.accept("escape", self.close_app)  # Chiude l'app quando si preme "Esc"
        self.accept("r", self.toggle_rotation)  # Ferma/Riprende la rotazione quando si preme "r"
        self.accept("q", self.close_app)  # Chiude l'app quando si preme "q"
        
    def rotate_model(self, task):
        # Incrementa l'angolo di rotazione lungo l'asse delle Y
        self.heading_angle += 1
        
        # Applica la rotazione al modello
        self.model.setHpr(self.heading_angle, 90, 0)
        
        # Restituisci "cont" per indicare che il task deve continuare ad aggiornarsi
        return Task.cont
    
    def toggle_rotation(self):
        if self.rotate_task.is_alive():
            # Ferma la rotazione del modello
            taskMgr.remove(self.rotate_task)
        else:
            # Riprende la rotazione del modello
            self.rotate_task = taskMgr.add(self.rotate_model, "rotate_model")
    
    def close_app(self):
        # Chiude l'applicazione
        sys.exit()
        
    def scale_model(self):
        bounds = self.model.get_tight_bounds()
        model_width = bounds[1].getX() - bounds[0].getX()
        model_height = bounds[1].getY() - bounds[0].getY()
        model_depth = bounds[1].getZ() - bounds[0].getZ()
        
        # Calcola la dimensione massima tra larghezza, altezza e profondità del modello
        max_dimension = max(model_width, model_height, model_depth)
        print(max_dimension)
        index_scale= 5/max_dimension
        self.model.setScale(index_scale)

app = MyApp()
app.run()


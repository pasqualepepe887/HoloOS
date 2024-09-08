from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, DirectionalLight, AmbientLight, Vec4, Quat
from direct.task import Task
import sys
import os

# pip install panda3d

# Note: if you change the model and you don't see any change, try to clean the cache: rm -r .cache/panda3d
path_model3d = "sword.obj"

# Change it depending on where you have the module
base_folder = os.path.dirname(os.path.abspath(__file__))
PATH_TO_BODYNODESHOST = "../body-nodes-host/modules/pythonlib"
PATH_TO_BODYNODESCOMMON = "../body-nodes-host/body-nodes-common"
sys.path.append(PATH_TO_BODYNODESHOST)
sys.path.append(PATH_TO_BODYNODESCOMMON)

try:
    import bnwifibodynodeshost as bodynodeshost
except ModuleNotFoundError:
    print( "__________________________")
    print( "You are missing the body-nodes-host python modules.")
    print( "You need to set the PATH_TO_BODYNODESHOST to the path" )
    print( "of where you clone body-nodes-host. The clone command is:" )
    print( "   git clone git@github.com:ManuDev9/body-nodes-host.git")
    print( "   OR")
    print( "   git clone https://github.com/ManuDev9/body-nodes-host.git")
    print( "__________________________")
    raise

import bnutils

orientation_vals = None

class KatanaBodynodeListener(bodynodeshost.BodynodeListener):
    def __init__(self):
        super().__init__()
        print("This the KatanaBodynodeListener")

    def onMessageReceived(self, player, bodypart, sensortype, value):
        #print("onMessageReceive: player="+player + " bodypart="+bodypart + " sensortype="+sensortype + " value="+str(value))
        global orientation_vals
        orientation_vals = value

    def isOfInterest(self, player, bodypart, sensortype):
        return bodypart == "katana"

bncommunicator = bodynodeshost.BnWifiHostCommunicator()
bnklistener = KatanaBodynodeListener()
bndata = bnutils.BnReorientAxis()
bndata.config( [0, 2, 1, 3], [-1, -1, 1, 1] )

class BnKatanaGameApp(ShowBase):
    def __init__(self):
        # Chiama il costruttore di ShowBase
        ShowBase.__init__(self)
        
        # Specifica la modalità fullscreen e altre proprietà della finestra
        props = WindowProperties()
        props.setSize(1280, 960)  # Imposta la dimensione della finestra se non in modalità fullscreen
        props.setFullscreen(False)  
        props.setTitle("3drender")  # Imposta il titolo della finestra
        self.win.requestProperties(props)
        
        # Imposta il colore di sfondo su nero
        self.win.setClearColor((0, 0, 0, 1))
        
        # Carica il modello in formato OBJ
        self.model = self.loader.loadModel(path_model3d)

        self.model.setScale(0.3)
        self.scale_model()

        # Rimuovi tutte le luci
        self.render.clearLight()
        
        # Imposta la posizione del modello nella scena
        self.model.reparentTo(self.render)
        self.model.setPos(0, 40, -7)
        self.model.setColor((1, 0, 0, 1)) 
        
        self.orientation_change_task = taskMgr.add(self.orientation_change, "orientation_change_task")

        # Add ambient light
        ambient_light = AmbientLight('ambient_light')
        ambient_light.setColor((0.3, 0.3, 0.3, 1))  # Light gray color
        ambient_light_node = self.render.attachNewNode(ambient_light)
        self.render.setLight(ambient_light_node)

        # Add directional light
        directional_light = DirectionalLight('directional_light')
        directional_light.setColor((1, 1, 1, 1))  # White light
        directional_light.setDirection((-1, -1, -1))  # Light direction
        directional_light_node = self.render.attachNewNode(directional_light)
        self.render.setLight(directional_light_node)
        
        # Optionally, add a shadow caster and receiver
        self.model.setShaderAuto()  # Enable shaders
        self.start_q = None        

        # Registra i key binding
        self.accept("escape", self.close_app)  # Chiude l'app quando si preme "Esc"
        self.accept("q", self.close_app)  # Chiude l'app quando si preme "q"

        # Registra eventi della finestra
        self.accept("window-event", self.windowEventHandler)
    
    def orientation_change(self, task):

        global orientation_vals
        global bndata

        #print(orientation_vals)
        if orientation_vals == None:
            return Task.cont

        if orientation_vals == "reset":
            self.start_q = None
            return Task.cont

        new_orientation_vals = orientation_vals.copy()
        bndata.apply( new_orientation_vals )

        orientation_q = Quat(new_orientation_vals[0], new_orientation_vals[1], new_orientation_vals[2], new_orientation_vals[3])

        if self.start_q == None:
            self.start_q = Quat()
            self.start_q.invertFrom(orientation_q)

        orientation_q = self.start_q * orientation_q

        # Applica la rotazione al modello
        self.model.setQuat(orientation_q)
        
        # Restituisci "cont" per indicare che il task deve continuare ad aggiornarsi
        return Task.cont
    
    
    def windowEventHandler(self, window):
        if window is not None:
            if not window.getProperties().getOpen():
                self.close_app()  # Cleanly exit the application

    def close_app(self):
        # Chiude l'applicazione
        bncommunicator.stop()
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

app = BnKatanaGameApp()
bncommunicator.start(["BN"])
bncommunicator.addListener(bnklistener)
app.run()



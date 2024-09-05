from direct.showbase.ShowBase import ShowBase
from panda3d.core import Point3, AmbientLight, DirectionalLight, PointLight,Material,Texture

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Imposta il colore di sfondo su nero
        self.setBackgroundColor(0, 0, 0)

        # Carica il modello del panda
        self.model = self.loader.loadModel("/home/HoloOS/GUI_TK/cow2.obj")
        self.model.reparentTo(self.render)
        
        # Scala e posizione il modello
        self.model.setScale(0.5, 0.5, 0.5)
        self.model.setPos(Point3(0, 10, 0))

        # Aggiungi una luce ambientale
        self.ambient_light = AmbientLight("ambient_light")
        self.ambient_light.setColor((0.2, 0.2, 0.2, 1))
        self.ambient_light_node_path = self.render.attachNewNode(self.ambient_light)
        self.render.setLight(self.ambient_light_node_path)

        # Aggiungi una luce direzionale
        self.directional_light = DirectionalLight("directional_light")
        self.directional_light.setColor((0.8, 0.8, 0.8, 1))
        self.directional_light_node_path = self.render.attachNewNode(self.directional_light)
        self.directional_light_node_path.setHpr(45, -45, 0)
        self.render.setLight(self.directional_light_node_path)

        # Aggiungi una luce puntiforme
        self.point_light = PointLight("point_light")
        self.point_light.setColor((1, 1, 1, 1))
        self.point_light_node_path = self.render.attachNewNode(self.point_light)
        self.point_light_node_path.setPos(0, 0, 10)
        self.render.setLight(self.point_light_node_path)
        material = Material()
        material.setDiffuse((1, 1, 1, 1))  # Imposta il colore diffuso del materiale
        
        # Assegna il materiale al modello
        self.model.setMaterial(material)

        texture = self.loader.loadTexture("base_texture.jpg")

        # Applica la texture al modello
        self.model.setTexture(texture)

        # Avvicina la telecamera al modello
        self.camera.setPos(30, -800, 5)
        
        # Ruota il modello continuamente
        self.taskMgr.add(self.spin_model, "spin_model_task")

    def spin_model(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (3.14159 / 180.0)
        self.model.setHpr(angleDegrees, 0, 0)
        return task.cont

app = MyApp()
app.run()

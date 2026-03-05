from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window

Config.set('graphics','resizable',0)
Window.clearcolor =(0,0,0,)

class nombre22_22App(App):
    pass


class estilo33333 (BoxLayout):
    mensaje = StringProperty("Hola desde Kivy")


if __name__ == "__main__":
    nombre22_22App().run()

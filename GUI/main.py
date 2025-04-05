from kivymd.app import MDApp
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.user_crud import *
from login_logout import *

    
class MyApp(MDApp):   
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Main(sm,name="modau"))
        sm.add_widget(Login(sm,name="login"))
        sm.add_widget(Register(sm,name="register"))
        sm.current = "modau"
        return sm


if __name__ == "__main__":
    MyApp().run()

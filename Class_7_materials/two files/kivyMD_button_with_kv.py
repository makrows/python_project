from kivymd.app import MDApp
from kivy.lang import Builder

class kivyMD_button_with_kv(MDApp):
    def build(self):
        return Builder.load_file("kivyMD_button_with_kv.kv")


kivyMD_button_with_kv().run()
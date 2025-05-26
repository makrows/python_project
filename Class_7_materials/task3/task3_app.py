from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.screen import MDScreen

Window.size = (350, 600)

class ContentNavigationDrawer(MDBoxLayout):
    pass

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))
    
    def on_release(self):
        self.parent.set_color_item(self)
        if self.text == "My files":
            app = MDApp.get_running_app()
            app.switch_screen("photos_screen")
        elif self.text == "Shared with me":
            app = MDApp.get_running_app()
            app.switch_screen("main_screen")

class DrawerList(MDList, ThemableBehavior):
    def set_color_item(self, instance_item):
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class MainScreen(MDScreen):
    pass

class PhotosScreen(MDScreen):
    pass

class Task3App(MDApp):
    dialog = None
    
    def build(self):
        return Builder.load_file('task3_app.kv')
    
    def switch_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name
        self.root.ids.nav_drawer.set_state("close")
    
    def on_start(self):
        icons_item = {
            "folder": "My files",
            "account-multiple": "Shared with me",
            "star": "Starred",
            "history": "Recent",
            "checkbox-marked": "Shared with me",
            "upload": "Upload",
        }
        for icon_name, item_name in icons_item.items():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=item_name)
            )
    
    def change_label_text(self):
        self.root.ids.my_label.text = "Text has been changed!"
    
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Important Message!",
                text="This is a popup dialog example",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="ACCEPT",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()
    
    def close_dialog(self, *args):
        self.dialog.dismiss()

if __name__ == '__main__':
    Task3App().run()
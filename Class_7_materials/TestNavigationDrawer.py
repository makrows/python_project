# TestNavigationDrawer.py
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList


from kivy.core.window import Window
Window.size = (350, 600)

#1 defines a custom list item class `ItemDrawer` which inherits from `OneLineIconListItem`.
# This allows for more control over the styling and behavior of each item in...
# the navigation drawer, including the addition of icons and custom text colors.

#2 The `on_start` method in the `TestNavigationDrawer` class is used to dynamically...
# populate the drawer with items. It uses a dictionary of icons and labels...
# to create and add multiple `ItemDrawer` widgets to the `DrawerList`.

#3 In `DrawerList`, the method `set_color_item` changes the text color of the ...
# selected item to indicate which menu item is active. This provides a...
# visual information to the user about the current selection

#4 The `ContentNavigationDrawer` includes an `AnchorLayout` and `ScrollView` within ...
# it. The `AnchorLayout` contains an image that serves as an avatar, while the...
# `ScrollView` allows the drawer content to be scrollable if it exceeds the screen height.

KV = '''
# Menu item in the DrawerList list.
<ItemDrawer>: #------------------------1 (and below)
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)

    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color


<ContentNavigationDrawer>: #---------------4
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "56dp", "56dp"
            source: "landscape.jpg"

    MDLabel:
        text: "KivyMD library"
        font_style: "Button"
        adaptive_height: True

    MDLabel:
        text: "kivydevelopment@gmail.com"
        font_style: "Caption"
        adaptive_height: True

    ScrollView:

        DrawerList:
            id: md_list



MDScreen:

    MDNavigationLayout:

        ScreenManager:

            MDScreen:

                MDBoxLayout:
                    orientation: 'vertical'

                    MDTopAppBar:
                        title: "Navigation Drawer"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]

                    Widget:


        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                id: content_drawer
'''


class ContentNavigationDrawer(MDBoxLayout):
    pass


class ItemDrawer(OneLineIconListItem): #------------------1
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(MDList, ThemableBehavior): #-------------3
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class TestNavigationDrawer(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self): #-------------------2
        icons_item = {
            "folder": "My files",
            "account-multiple": "Shared with me",
            "star": "Starred",
            "history": "Recent",
            "checkbox-marked": "Shared with me",
            "upload": "Upload",
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )


TestNavigationDrawer().run()
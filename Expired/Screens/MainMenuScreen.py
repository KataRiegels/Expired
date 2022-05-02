# from audioop import tostereo
# from kivy.uix.screenmanager import Screen
# from kivy.app import App

# # for makng button work
# from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
# # from ..Widgets.Button import Button
# # from ..Items.Items import Items
# from kivy.uix.button import Button
# from functools import partial
# from kivymd.uix.screen import MDScreen

from . import MScreen

# class MenuScreen():
#     pass

class MenuScreen(MScreen):
    def __init__(self,**args):
        super().__init__(**args)


    

    def changeToList(self):
        self.manager.current = 'list'
        listscreen = self.manager.current_screen
        listscreen.startScreen()



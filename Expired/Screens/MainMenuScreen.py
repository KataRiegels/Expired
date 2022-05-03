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
from sqlite3 import Date
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from . import MScreen
from kivymd.app import MDApp
# class MenuScreen():
#     pass

class DateLayout(RelativeLayout):
    def __init__(self, **kw):
        
        super().__init__(**kw)
        
    def createItem(self,item):
        self.ids.expiry_date_lbl = item.expiryDate.toString()
        self.ids.product_name_lbl = item.productName
    
    pass


class DatesLayout(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def addItem(self,item):
        self.add_widget(item)
        pass

class MenuScreen(MScreen):
    def __init__(self,**args):
        super().__init__(**args)

    def on_pre_enter(self, *args):
        for item in MDApp.get_running_app().fridge.sortedFridgeListDate:
            food = DateLayout()
            food.createItem(item)
            # food.ids.exp_date_lbl = item.expiryDate.toString()
            # food.ids.product_name_lbl = item.productName
            # self.ids.dates_layout.addItem(food)
            # self.ids.dates_layout
        print(self.ids)
        # self.ids.test
        return super().on_pre_enter(*args)

    

    def changeToList(self):
        self.manager.current = 'list'
        listscreen = self.manager.current_screen
        listscreen.startScreen()



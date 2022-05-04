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
        
    def createItem(self,item):
        self.ids.expiry_date_lbl.text = item.expiryDate.toString()
        self.ids.product_name_lbl.text = item.productName
    
    pass


class DatesLayout(BoxLayout):
    
    # def __init__(self,item = None, _owner = None):
    #     self.item = item
    #     self._owner = _owner
    #     super().__init__()
    
    def addItem(self,item):
        # item.exp_date_lbl = self._owner.expiryDate.toString()
        # item.product_name_lbl = self._owner.productName
        # print(item.ids.expiry_date_lbl.tex)
        self.add_widget(item)
        pass

class MenuScreen(MScreen):
    def __init__(self,**args):
        super().__init__(**args)

    def on_pre_enter(self, *args):
        return super().on_pre_enter(*args)

    def prepareMenu(self):
        self.ids.dates_layout.clear_widgets()
        for item in MDApp.get_running_app().fridge.sortedFridgeListDate:
            food = DateLayout()
            food.createItem(item)
            # food.ids.exp_date_lbl = item.expiryDate.toString()
            # food.ids.product_name_lbl = item.productName
            self.ids.dates_layout.addItem(food)
            if len(self.ids.dates_layout.children)>3:
                break
            # self.ids.dates_layout
        # self.ids.test
        

    def changeToList(self):
        self.manager.current = 'list'
        listscreen = self.manager.current_screen
        listscreen.startScreen()



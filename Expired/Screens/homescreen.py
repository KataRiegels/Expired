# from audioop import tostereo
# from kivy.uix.screenmanager import Screen
# from kivy.app import App

# # for makng button work
# from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
# # from ..widgets.Button import Button
# # from ..Items.Items import Items
# from kivy.uix.button import Button
# from functools import partial
# from kivymd.uix.screen import MDScreen
from sqlite3 import Date
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from . import MyScreen
from kivymd.app import MDApp
# class HomeScreen():
#     pass

class DateLayout(RelativeLayout):
        
    def createItem(self,item):
        self.ids.expiry_date_lbl.text = item.expiry_date.as_string()
        self.ids.product_name_lbl.text = item.product_name
    
    pass


class DatesLayout(BoxLayout):
    
    # def __init__(self,item = None, _owner = None):
    #     self.item = item
    #     self._owner = _owner
    #     super().__init__()
    
    def addItem(self,item):
        self.add_widget(item)
        pass

class HomeScreen(MyScreen):
    
    entered = False
    
    def __init__(self,**args):
        super().__init__(**args)

    def on_pre_enter(self, *args):
        return super().on_pre_enter(*args)

    # def on_enter(self, *args):
    #     if not self.entered:
    #         self.entered = True
    #         self.create_selection_list()
    #     return super().on_enter(*args)

    # def create_selection_list(self):
    #     # MDApp.get_running_app().list_screen.ids.select_view.create_item_list_widget()
    #     app = MDApp.get_running_app()
    #     print("hello")
        
    #     pass

    # def prepareMenu(self):
    def initiateScreen(self):
        self.ids.dates_layout.clear_widgets()
        for item in MDApp.get_running_app().fridge.sorted_fridge_list:
            food = DateLayout()
            food.createItem(item)
            self.ids.dates_layout.addItem(food)
            if len(self.ids.dates_layout.children)>5:
                break
            
    def updated_fridge(self):
        self.initiateScreen()
        # return super().updated_fridge()
            # self.ids.dates_layout
        # self.ids.test
        

    def changeToList(self):
        self.manager.current = 'list'
        listscreen = self.manager.current_screen
        listscreen.startScreen()



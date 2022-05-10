

import os
import kivy
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from Screens.ListScreen import ListScreen
from Screens.ScanScreen import ScanScreen
from Screens.SettingsScreen import SettingsScreen
from Screens.CalenderScreen import CalenderScreen
from kivy.config import Config
from kivymd.uix.screen import MDScreen
# from kivymd.uix.label import MDLabel
from Screens.MainMenuScreen import *
# from Screens.MainMenuScreen import *
# from kivymd.uix.textfield import MDTextField
from Items import *
from Widgets.Bars import *
from kivy.uix.screenmanager import *
from kivy.core.text import LabelBase
from kivy.uix.scrollview import DampedScrollEffect
from colors import colors
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex


# class MyAppClass(FloatLayout):#its a FloatLayout in my case
#     _screen_manager=ObjectProperty(None)
#     def __init__(self,**kwargs):
#         super(MyAppClass,self).__init__(**kwargs)
#         #code goes here and add:




# from kivymd.uix.transition.transition import MDFadeSlideTransition
# kivymd.uix.transition.transition.MDFadeSlideTransition

LabelBase.register(name='ExpiredFont', fn_regular='Resources/custom.ttf')
# LabelBase.register(name='BestBefore', fn_regular='Resources/bestbefore-regular.ttf')
# LabelBase.register(name='BestBefore', fn_regular='Resources/bestbefore.ttf')
LabelBase.register(name='BestBefore', fn_regular='Resources/Dited.otf')

def building():
    Builder.load_file('Screens/mainmenuscreen.kv')
    Builder.load_file('Widgets/itemlistdisplay.kv')
    Builder.load_file('Screens/listscreen.kv')
    Builder.load_file('Screens/scanscreen.kv')

    Builder.load_file('Screens/settingsscreen.kv')
    Builder.load_file('Screens/calenderscreen.kv')
    Builder.load_file('Widgets/bars.kv')
    return Builder.load_file('main_screen.kv')
# Config.set(' graphics', 'resizable', '0')
# Config.set('graphics', 'height', '600')
# Config.set('graphics', 'width', '300')

# from kivy.core.window import Window

Window.softinput_mode = "below_target"

# colors = {
#     "Teal": {
#         "50": "#e4f8f9",
#         "100": "#bdedf0",
#         "200": "#97e2e8",
#         "300": "#79d5de",
#         "400": "#6dcbd6",
#         "500": "#6ac2cf",
#         "600": "#63b2bc",
#         "700": "#5b9ca3",
#         "800": "#54888c",
#         "900": "#486363",
#         "A100": "#bdedf0",
#         "A200": "#97e2e8",
#         "A400": "#6dcbd6",
#         "A700": "#5b9ca3",
#     },
#     "Blue": {
#         "50": "#e3f3f8",
#         "100": "#b9e1ee",
#         "200": "#91cee3",
#         "300": "#72bad6",
#         "400": "#62acce",
#         "500": "#589fc6",
#         "600": "#5191b8",
#         "700": "#487fa5",
#         "800": "#426f91",
#         "900": "#35506d",
#         "A100": "#b9e1ee",
#         "A200": "#91cee3",
#         "A400": "#62acce",
#         "A700": "#487fa5",
#     },
#     "Red": {
#         "50": "#FFEBEE",
#         "100": "#FFCDD2",
#         "200": "#EF9A9A",
#         "300": "#E57373",
#         "400": "#EF5350",
#         "500": "#F44336",
#         "600": "#E53935",
#         "700": "#D32F2F",
#         "800": "#C62828",
#         "900": "#B71C1C",
#         "A100": "#FF8A80",
#         "A200": "#FF5252",
#         "A400": "#FF1744",
#         "A700": "#D50000",
#     },
#     "Light": {
#         "StatusBar": "#E0E0E0",
#         "AppBar": "#F5F5F5",
#         "Background": "#FAFAFA",
#         "CardsDialogs": "#FFFFFF",
#         "FlatButtonDown": "#cccccc",
#     },
#     "Dark": {
#         "StatusBar": "#000000",
#         "AppBar": "#212121",
#         "Background": "#303030",
#         "CardsDialogs": "#424242",
#         "FlatButtonDown": "#999999",
#     }
# }

class Lay(BoxLayout):
    pass

class TestApp(MDApp):
    def build(self):
        
        manager = building()
        self.enable_swipe = True
        bar = manager.ids.nav_bar
        menuscreen = bar.ids.menu_tab
        bar.ids.tab_manager.transition = SlideTransition(direction = "right") 
        self.sm = bar.ids.tab_manager
        self.bar = bar
        
        # self.primary_light_hue = 
        # self.primary_dark_hue = 
        self.theme_cls.accent_palette = "Red"
        # self.theme_cls.accent_hue = "50"
        # self.theme_cls.accent_light_hue = "50"
        # self.theme_cls.accent_dark_hue = "500"
        self.theme_cls.colors = colors
        # self.theme_cls.primary_hue = "900"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"    
        self.theme_cls.primary_light_hue = "50"    
        self.theme_cls.primary_dark_hue = "500"
        self.secondary_dark = get_color_from_hex(self.theme_cls.colors[self.theme_cls.primary_palette][self.theme_cls.primary_light_hue])
            
        self.items = Items("data.json")
        self.items.openFridge()
        self.fridge = self.items
        self.bar.ids.menu_tab.prepareMenu()
        # self.theme_cls.bg_normal = "Teal"
        # self.theme_cls.accent_palette = "Red"
        # self.theme_cls.accent_dark_hue = "50"    
        # Window.bind(on_keyboard=self.Android_back_click)
        Window.bind(on_keyboard=self.Android_back_click)

        return manager
        # return Lay()
    
    def change_theme(self): 
        if self.theme_cls.primary_palette == "Blue":
            self.theme_cls.primary_palette = "Red"
        elif self.theme_cls.primary_palette == "Red":
            self.theme_cls.primary_palette = "Blue"
        
    def Android_back_click(self,window,key,*largs):
        if key == 27:
            self.bar.back_screen()
            # self.bar.switch_tab(self.bar.get_screen_from_order(self.bar.current_tab).name)#you can create a method here to cache in a list the number of screens and then pop the last visited screen.
            return True
        
    def stop(self, *largs):
        self.bar.ids.scan_tab.on_leave()
        return super().stop(*largs)
        
        
        
        
TestApp().run()



# cake = Item("Cake",Date(2530,5,9),"4")
# pizza = Item("Pizza",Date(2050,2,6),"2")

# fridge = Items(jsonfile = "data.json")
# fridge.addItem(cake)
# fridge.addItem(pizza)
# fridge.sortAscendingDate()
# fridge.convertToJSON()
# jsondic = fridge.createJSON()


# dic = fridge.loadJSON()
# fridge.jsonFormatToItemFormat(dic)
# items = Items("data copy.json")
# items.jsonFormatToItemFormat()
# print(items.fridge)
# items.removeItem("5")
# print(items.fridge)
# # items.convertToJSON()
# # items.createJSON()

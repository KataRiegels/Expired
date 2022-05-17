

import os
import kivy
import kivymd
print(kivymd.__version__)
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
import csv


LabelBase.register(name='ExpiredFont', fn_regular='Resources/custom.ttf')
LabelBase.register(name='BestBefore', fn_regular='Resources/Dited.otf')

def building():
    Builder.load_file('Widgets/itemlistdisplay.kv')
    Builder.load_file('Screens/mainmenuscreen.kv')
    Builder.load_file('Screens/settingsscreen.kv')
    Builder.load_file('Screens/listscreen.kv')
    Builder.load_file('Screens/scanscreen.kv')

    Builder.load_file('Screens/calenderscreen.kv')
    Builder.load_file('Widgets/bars.kv')
    return Builder.load_file('main_screen.kv')
# Config.set(' graphics', 'resizable', '0')
# Config.set('graphics', 'height', '600')
# Config.set('graphics', 'width', '300')


Window.softinput_mode = "below_target"

def setTheme(app):
    with open('theme.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = []
        data = next(csv_reader)
        primary = data[0]
        style = data[1]
            
    app.theme_cls.accent_palette = "Red"
    app.theme_cls.colors = colors
    app.theme_cls.primary_hue = "900"
    app.theme_cls.theme_style = style
    app.theme_cls.primary_palette = primary    
    app.theme_cls.primary_light_hue = "100"    
    app.theme_cls.primary_dark_hue = "500"
    app.secondary_dark = get_color_from_hex(app.theme_cls.colors[app.theme_cls.primary_palette][app.theme_cls.primary_light_hue])
      



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
        setTheme(self)
        self.items = Items("data.json")
        self.items.openFridge()
        self.fridge = self.items
        # self.bar.ids.menu_tab.initiateScreen()
        for child in self.bar.ids.tab_manager.screens:
            child.initiateScreen()
        self.list_screen = bar.ids.list_tab
        self.scan_screen = bar.ids.scan_tab
        self.settings_screen = bar.ids.settings_tab
        self.menu_screen = bar.ids.menu_tab
        Window.bind(on_keyboard=self.Android_back_click)

        return manager
    
    def Android_back_click(self,window,key,*largs):
        if key == 27:
            self.bar.back_screen()
            return True
        
    def stop(self, *largs):
        self.bar.ids.scan_tab.on_leave()
        with open('theme.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow([self.theme_cls.primary_palette,self.theme_cls.theme_style])
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

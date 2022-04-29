from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivymd.app import MDApp
from Screens.MScreen import PrimaryScreen
from Screens.MainMenuScreen import MenuScreen
from Screens.ScanScreen import ScanScreen
from Screens.SettingsScreen import SettingsScreen
from Screens.CalenderScreen import CalenderScreen
from kivy.core.text import LabelBase
from kivy.config import Config
from Items import *
from kivymd.uix.textfield import MDTextField
# from kivymd.uix.transition.transition import MDFadeSlideTransition
# kivymd.uix.transition.transition.MDFadeSlideTransition

LabelBase.register(name='ExpiredFont', fn_regular='Resources/custom.ttf')
Builder.load_file('Screens/listscreen.kv')
Builder.load_file('Screens/mainmenuscreen.kv')
from Screens.ListScreen import ListScreen
Builder.load_file('Widgets/itemlistdisplay.kv')
Builder.load_file('Screens/scanscreen.kv')
Builder.load_file('Widgets/bars.kv')

Builder.load_file('Screens/settingsscreen.kv')
Builder.load_file('Screens/calenderscreen.kv')
Builder.load_file('main_screen.kv')
# Config.set(' graphics', 'resizable', '0')
# Config.set('graphics', 'height', '600')
# Config.set('graphics', 'width', '300')

# from kivy.core.window import Window

# Window.softinput_mode = "below_target"

import json

colors = {
    "Teal": {
        "50": "e4f8f9",
        "100": "bdedf0",
        "200": "97e2e8",
        "300": "79d5de",
        "400": "6dcbd6",
        "500": "6ac2cf",
        "600": "63b2bc",
        "700": "5b9ca3",
        "800": "54888c",
        "900": "486363",
        "A100": "bdedf0",
        "A200": "97e2e8",
        "A400": "6dcbd6",
        "A700": "5b9ca3",
    },
    "Blue": {
        "50": "e3f3f8",
        "100": "b9e1ee",
        "200": "91cee3",
        "300": "72bad6",
        "400": "62acce",
        "500": "589fc6",
        "600": "5191b8",
        "700": "487fa5",
        "800": "426f91",
        "900": "35506d",
        "A100": "b9e1ee",
        "A200": "91cee3",
        "A400": "62acce",
        "A700": "487fa5",
    },
    "Red": {
        "50": "FFEBEE",
        "100": "FFCDD2",
        "200": "EF9A9A",
        "300": "E57373",
        "400": "EF5350",
        "500": "F44336",
        "600": "E53935",
        "700": "D32F2F",
        "800": "C62828",
        "900": "B71C1C",
        "A100": "FF8A80",
        "A200": "FF5252",
        "A400": "FF1744",
        "A700": "D50000",
    },
    "Light": {
        "StatusBar": "E0E0E0",
        "AppBar": "F5F5F5",
        "Background": "FAFAFA",
        "CardsDialogs": "FFFFFF",
        "FlatButtonDown": "cccccc",
    },
    "Dark": {
        "StatusBar": "000000",
        "AppBar": "212121",
        "Background": "303030",
        "CardsDialogs": "424242",
        "FlatButtonDown": "999999",
    }
}

# 
class TestApp(MDApp):
    def build(self):
        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Teal"
        # self.theme_cls.primary_palette = "Green"  # "Purple", "Red"
        # self.theme_cls.primary_hue = "200"  # "500"
        self.items = Items("data.json")
        # items.jsonFo rmatToItemFormat()
        self.items.openFridge()
        # sm = ScreenManager()
        sm = PrimaryScreen()
        self.sm = sm
        sm.fridge = self.items # so it can be accessed by other screens
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ListScreen(name='list'))
        sm.add_widget(ScanScreen(name='scan'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(CalenderScreen(name='calender'))
        return sm

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

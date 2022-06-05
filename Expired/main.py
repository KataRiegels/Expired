from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from screens.listscreen import ListScreen
from screens.scanscreen import ScanScreen
from screens.settingsscreen import SettingsScreen
from screens.homescreen import *
from items import *
from widgets.bars import *
from kivy.uix.screenmanager import *
from kivy.core.text import LabelBase
from resources.colors import colors
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex
import csv

# Config.set('graphics', 'resizable', '0')
# Config.set('graphics', 'height', '600')
# Config.set('graphics', 'width', '300')

# LabelBase.register(name='ExpiredFont', fn_regular='resources/custom.ttf')
LabelBase.register(name='BestBefore', fn_regular='resources/Dited.otf')

def building():
    Builder.load_file('widgets/item_display.kv')
    Builder.load_file('screens/homescreen.kv')
    Builder.load_file('screens/settingsscreen.kv')
    Builder.load_file('screens/listscreen.kv')
    Builder.load_file('screens/scanscreen.kv')

    Builder.load_file('widgets/bars.kv')
    return Builder.load_file('main_screen.kv')


Window.softinput_mode = "below_target"

def setTheme(app):
    with open('save_files/theme.csv') as csv_file:
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
      



class Root(BoxLayout):
    pass

class ExpiringFoodApp(MDApp):
    def build(self):
        manager2 = building()
        manager = Root()
        self.enable_swipe = True
        bar = manager.ids.nav_bar
        menuscreen = bar.ids.menu_tab
        bar.ids.tab_manager.transition = SlideTransition(direction = "right") 
        self.sm = bar.ids.tab_manager
        self.bar = bar
        setTheme(self)
        print("LOADING JSON FILE")
        self.items = Items("save_files/data.json")
        print("finished loading JSON")
        self.items.openFridge()
        self.fridge = self.items
        self.list_screen = bar.ids.list_tab
        self.scan_screen = bar.ids.scan_tab
        self.settings_screen = bar.ids.settings_tab
        self.menu_screen = bar.ids.menu_tab
        self.menu_screen.initiateScreen()
        # self.list_screen.ids.select_view.create_item_list_widget()
        # Clock.schedule_once(self.make_widget,1)
        # self.make_widget(2)
        Window.bind(on_keyboard=self.back_click)

        return manager
        # return root
    def on_start(self,**kwargs):
        # Clock.schedule_once(self.make_widget,3)
        # self.make_widget(2)
        self.test()
        pass
    
    @mainthread
    def test(self):
        # self.make_widget(2)
        Clock.schedule_once(self.make_widget,.1)
        
        pass
    
    # @mainthread
    def make_widget(self, value):
        print("loading...")
        # self.list_screen.ids.select_view.create_item_list_widget()
        print("Created list view")
        for child in self.bar.ids.tab_manager.screens:
            if not child == self.menu_screen:
                child.initiateScreen()
        print("now it ran")
            
        pass
    
    def back_click(self,window,key,*largs):
        if key == 27:
            self.bar.back_screen()
            return True
        
    def update_fridge(self):
        for screen in self.bar.ids.tab_manager.screens:
            screen.updated_fridge()
        
        
    def stop(self, *largs):
        self.bar.ids.scan_tab.on_pre_leave()
        return super().stop(*largs)
        
        
        
        
ExpiringFoodApp().run()



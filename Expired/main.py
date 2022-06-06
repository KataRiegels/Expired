
from kivy.utils  import platform
if platform != 'android':
    # Needs to be set before importing Window - Won't work otherwise
    from kivy.config import Config
    # Sets screen size
    Config.set('graphics', 'resizable', '0')
    Config.set('graphics', 'height', '600')
    Config.set('graphics', 'width', '350')

from kivy.clock             import Clock, mainthread
from kivy.lang              import Builder
from kivy.core.window       import Window
from kivy.core.text         import LabelBase
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.boxlayout     import BoxLayout
from kivy.utils             import get_color_from_hex
from kivymd.app             import MDApp

from resources.colors       import colors # File containing the theme color definitions
from items                  import Items
from screens                import ListScreen, ScanScreen, SettingsScreen, HomeScreen
import csv

Window.softinput_mode = "below_target" # Makes the screen go upwards when opening keyboard
LabelBase.register(name='BestBefore', fn_regular='resources/Dited.otf')

class Root(BoxLayout):
    pass

class ExpiringFoodApp(MDApp):
    def build(self):
        building_kv()                      
        setTheme(self)
        root_widget         = Root()
        
        self.enable_swipe   = True
        self.bar            = root_widget.ids.nav_bar           # Navigation bar
        self.sm             = self.bar.ids.tab_manager          # The ScreenManager from the navigation bar
        self.sm.transition  = SlideTransition()                 # Settings the screen change animation to sliding
        self.fridge         = Items("save_files/fridge.json")     # Creating the fridge instance
        self.fridge.open_fridge()                               # Loading the JSON file with the food items
        
        # Adding screens to the app
        self.list_screen     = self.bar.ids.list_tab
        self.scan_screen     = self.bar.ids.scan_tab
        self.settings_screen = self.bar.ids.settings_tab
        self.menu_screen     = self.bar.ids.menu_tab
        self.menu_screen.initiate_screen()
        
        Window.bind(on_keyboard=self.back_click)
        return root_widget

    """ Triggers when app loaded """    
    def on_start(self,**kwargs):
        self.when_loaded()
    
    """ Needs method on mainthread (first triggers when app is and main loop starts) """
    @mainthread
    def when_loaded(self):
        # Needs a tiny delay in order to first trigger method after first screen is shown
        Clock.schedule_once(self.initiate_remaining_screens,.1)
    
    """ Some screens need a method run to add certain functionalities/wdigets """
    def initiate_remaining_screens(self, value):
        for child in self.sm.screens:
            if not child == self.menu_screen:
                child.initiate_screen()
    
    """ When back key on Android device is clicked """
    def back_click(self,window,key,*largs):
        if key == 27:
            self.bar.back_screen()
            return True
    
    """ Updating fridge for everything needed """
    def update_fridge(self):
        for screen in self.sm.screens:
            screen.updated_fridge()
    
    """ Making sure camera is disabled when exiting app """
    def on_stop(self):
        self.bar.ids.scan_tab.on_pre_leave()
        return super().on_stop()

""" Builds all the .kv files """
def building_kv():
    Builder.load_file('widgets/item_display.kv')
    Builder.load_file('screens/homescreen.kv')
    Builder.load_file('screens/settingsscreen.kv')
    Builder.load_file('screens/listscreen.kv')
    Builder.load_file('screens/scanscreen.kv')
    Builder.load_file('widgets/bars.kv')
    return Builder.load_file('root.kv')


""" Sets the theme based on the saved theme """
def setTheme(app):
    with open('save_files/theme.csv') as csv_file:
        csv_reader  = csv.reader(csv_file)
        data        = []
        data        = next(csv_reader)
        primary     = data[0]
        style       = data[1]
            
    app.theme_cls.colors            = colors
    app.theme_cls.theme_style       = style
    app.theme_cls.primary_palette   = primary    
    app.theme_cls.primary_hue       = "900"
    app.theme_cls.primary_light_hue = "100"    
    app.theme_cls.primary_dark_hue  = "500"

    
        
        
ExpiringFoodApp().run()



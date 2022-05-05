from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.bottomnavigation import MDBottomNavigation,MDBottomNavigationItem
from Widgets.Bars import MNavigationBar, NavigationItem
from gestures4kivy import CommonGestures

# class MyScreen(MDScreen):
class MyScreen(MDBottomNavigationItem,Screen,CommonGestures):
# class MyScreen(NavigationItem):
    # app = App.get_running_app()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.md_bg_color = MDApp.get_running_app().theme_cls.bg_light
         
        # self.sm = self.app.sm
        # self.add_widget(self.sm.bar)
        
    def cg_swipe_horizontal(self, touch, right):
        # MDApp.get_running_app().swipe_screen(right)
        self._parent.swipe_screen(right)
        
    def closeApp(self):
        MDApp.get_running_app().stop()
        
    # def on_tab_press(self, *args):
        
    #     return super().on_tab_press(*args)
        
        
    def initiateScreens(self):
        pass
        # bar = MNavigationBar()
        # self.add_widget(bar)
        # bar = MDBottomNavigation()
        
class PrimaryScreen(ScreenManager):
    # bar = Bars.MNavigationBar()
    pass
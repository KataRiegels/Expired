from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.toolbar import MDToolbar
from kivymd.app import MDApp

# for navigatio nheader
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
    AliasProperty
)
from kivy.utils import get_color_from_hex
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManagerException

from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.behaviors.backgroundcolor_behavior import (
    BackgroundColorBehavior,
    SpecificBackgroundColorBehavior,
)



class MNavigationBar(MDBottomNavigation):
    
    def __init__(self, **kwargs):
        self.latest_tabs = [1]
        self.current_tab = 1
        super().__init__(**kwargs)
    
    def updateBackList(self,current):
        print(self.latest_tabs)
        self.latest_tabs.append(current)
        if len(self.latest_tabs) > 4:
            self.latest_tabs.pop(0)
        return self.latest_tabs[-1]
        pass
    
    def get_screen_from_order(self,order):
        for tab in self.ids.tab_manager.screens:
            if tab.order == order:
                return tab
        
    def swipe_screen(self, right):
        # self.on_text_color_normal(None,MDApp.get_running_app().theme_cls.primary_light)
        sm = self.ids.tab_manager  
        current = sm.current_screen
        next_screen = current      
        if right:
            sm.transition.direction = 'right'
            if not current.order < 2:
                next_screen = self.get_screen_from_order(current.order-1)
        else:
            sm.transition.direction = 'left'
            if not current.order > 3:
                next_screen = self.get_screen_from_order(current.order+1)
            # self.switch_tab(next_screen)
        # self.current_tab = sm.get_screen(next_screen.name).order
        # self.updateBackList(current.order)
        # self.updateBackList(next_screen.order)
        self.current_tab = current.order
        self.switch_tab(next_screen.name)
    
    def back_screen(self):
        to_screen_order = self.current_tab
        to_screen = self.get_screen_from_order(to_screen_order)
        if self.current_tab == self.ids.tab_manager.current_screen.order:
            self.switch_tab("menu")
        else: self.switch_tab(to_screen.name)
        # current = self.get_screen_from_order(self.current_tab)
        # to_screen_order = self.latest_tabs[-2]
        # print(to_screen.order)
        # self.updateBackList(to_screen.order)
        # self.updateBackList(self.current_tab)
    
    def change_screen(self,to_screen):
        # self.on_text_color_normal(None,[1,1,1,1])
        sm = self.ids.tab_manager  
        current = sm.current_screen      
        if current.order < sm.get_screen(to_screen).order:
            sm.transition.direction = 'left'
        if current.order > sm.get_screen(to_screen).order:
            sm.transition.direction = 'right'
        # self.updateBackList(sm.get_screen(to_screen).order)
        # self.updateBackList(current.order)
        self.current_tab = current.order
        # self.current_tab = sm.get_screen(to_screen).order
        # self.current_tab = to_screen.order
    pass

    # def _get_disabled_hint_text_color(self, opposite=False):
    #     theme_style = self._get_theme_style(opposite)
    #     if theme_style == "Light":
    #         # color = get_color_from_hex("000000")
    #         color = get_color_from_hex("000000")
    #         color[3] = 0.38
    #         color[3] = 0.9
    #     elif theme_style == "Dark":
    #         color = get_color_from_hex("FFFFFF")
    #         color[3] = 0.50
    #         color[3] = 0.9
    #     return color

    # disabled_hint_text_color = AliasProperty(
    #     _get_disabled_hint_text_color, bind=["theme_style"]
    # )

""" I believe this is unnecessary - was used as superclass for MyScreen"""
class NavigationItem(MDBottomNavigationItem):
    
    pass


# class Toolbar(MDToolbar):
#     pass

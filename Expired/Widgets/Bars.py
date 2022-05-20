from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.bottomnavigation import MDBottomNavigationItem,MDBottomNavigationHeader
from kivymd.uix.toolbar import MDToolbar
from kivymd.app import MDApp

# for navigatio nheader
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import sp,dp
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

class MyBottomNavigationHeader(MDBottomNavigationHeader):
    def on_press(self) -> None:
        """Called when clicking on a panel item."""

        if self.theme_cls.material_style == "M2":
            Animation(_label_font_size=sp(14), d=0.1).start(self)
        elif self.theme_cls.material_style == "M3":
            Animation(
                _selected_region_width=dp(64),
                t="in_out_sine",
                d=0,
            ).start(self)
        Animation(
            _text_color_normal=self.theme_cls.primary_color
            # _text_color_normal=self.theme_cls.primary_dark_hue
            if self.text_color_active == [1, 1, 1, 1]
            else self.text_color_active,
            d=0.1,
        ).start(self)


class MNavigationBar(MDBottomNavigation):
    
    def __init__(self, **kwargs):
        self.latest_tabs = [1]
        self.current_tab = 1
        super().__init__(**kwargs)
    
    # def on_text_color_normal(
    #     self, instance_bottom_navigation, color: list
    # ) -> None:
    #     MDBottomNavigationHeader.text_color_normal = color
    #     for tab in self.ids.tab_bar.children:
    #         if not tab.active:
    #             tab._text_color_normal = color

    # def on_text_color_active(
    #     self, instance_bottom_navigation, color: list
    # ) -> None:
    #     MDBottomNavigationHeader.text_color_active = color
    #     self.text_color_active = color
    #     for tab in self.ids.tab_bar.children:
    #         tab.text_color_active = color
    #         if tab.active:
    #             # return
    #             tab._text_color_normal = color
    
    
    def on_press(self):
        Animation(_label_font_size=sp(14), d=0.1).start(self)
        Animation(
            _text_color_normal=self.theme_cls.primary_color,
            # if self.text_color_active == [1, 1, 1, 1]
            # else self.text_color_active,
            d=0.1,
        ).start(self)
    
    def updateBackList(self,current):
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
        self.current_tab = current.order
        self.switch_tab(next_screen.name)
    
    def back_screen(self):
        to_screen_order = self.current_tab
        to_screen = self.get_screen_from_order(to_screen_order)
        if self.current_tab == self.ids.tab_manager.current_screen.order:
            self.switch_tab("menu")
        else: self.switch_tab(to_screen.name)
    
    def change_screen(self,to_screen):
        sm = self.ids.tab_manager  
        current = sm.current_screen      
        if current.order < sm.get_screen(to_screen).order:
            sm.transition.direction = 'left'
        if current.order > sm.get_screen(to_screen).order:
            sm.transition.direction = 'right'
        self.current_tab = current.order
    pass


""" I believe this is unnecessary - was used as superclass for MyScreen"""
class NavigationItem(MDBottomNavigationItem):
    
    pass


# class Toolbar(MDToolbar):
#     pass

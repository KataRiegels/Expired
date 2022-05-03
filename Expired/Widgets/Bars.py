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
        self.updateBackList(next_screen.order)
        self.current_tab = current.order
        self.switch_tab(next_screen.name)
    
    def back_screen(self):
        # to_screen_order = self.current_tab
        current = self.get_screen_from_order(self.current_tab)
        to_screen_order = self.latest_tabs[-2]
        to_screen = self.get_screen_from_order(to_screen_order)
        # print(to_screen.order)
        self.updateBackList(to_screen.order)
        # self.updateBackList(self.current_tab)
        self.switch_tab(to_screen.name)
    
    def change_screen(self,to_screen):
        # self.on_text_color_normal(None,[1,1,1,1])
        sm = self.ids.tab_manager  
        current = sm.current_screen      
        if current.order < sm.get_screen(to_screen).order:
            sm.transition.direction = 'left'
        if current.order > sm.get_screen(to_screen).order:
            sm.transition.direction = 'right'
        self.updateBackList(sm.get_screen(to_screen).order)
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

class NavigationItem(MDBottomNavigationItem):
    
    pass


class Toolbar(MDToolbar):
    pass


class MDBottomNavigationHeader(ThemableBehavior, ButtonBehavior, AnchorLayout):
    opposite_colors = BooleanProperty(True)

    panel_color = ListProperty([1, 1, 1, 0])
    """Panel color of bottom navigation.

    :attr:`panel_color` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[1, 1, 1, 0]`.
    """

    tab = ObjectProperty()
    """
    :attr:`tab` is an :class:`~MDBottomNavigationItem`
    and defaults to `None`.
    """

    panel = ObjectProperty()
    """
    :attr:`panel` is an :class:`~MDBottomNavigation`
    and defaults to `None`.
    """

    active = BooleanProperty(False)

    text = StringProperty()
    """
    :attr:`text` is an :class:`~MDTab.text`
    and defaults to `''`.
    """

    text_color_normal = ListProperty([1, 1, 1, 1])
    """
    Text color of the label when it is not selected.

    :attr:`text_color_normal` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[1, 1, 1, 1]`.
    """

    text_color_active = ListProperty([1, 1, 1, 1])
    """
    Text color of the label when it is selected.

    :attr:`text_color_active` is an :class:`~kivy.properties.ListProperty`
    and defaults to `[1, 1, 1, 1]`.
    """

    _label = ObjectProperty()
    _label_font_size = NumericProperty("12sp")
    _text_color_normal = ListProperty([1, 1, 1, 1])
    _text_color_active = ListProperty([1, 1, 1, 1])

    def __init__(self, panel, height, tab):
        self.panel = panel
        self.height = height
        self.tab = tab
        super().__init__()
        self._text_color_normal = (
            self.theme_cls.disabled_hint_text_color
            if self.text_color_normal == [1, 1, 1, 1]
            else self.text_color_normal
        )
        self._label = self.ids._label
        self._label_font_size = sp(12)
        self.theme_cls.bind(disabled_hint_text_color=self._update_theme_style)
        self.active = False

    def on_press(self):
        Animation(_label_font_size=sp(14), d=0.1).start(self)
        Animation(
            _text_color_normal=self.theme_cls.primary_color
            if self.text_color_active == [1, 1, 1, 1]
            else self.text_color_active,
            d=0.1,
        ).start(self)

    def _update_theme_style(self, instance, color):
        """Called when the application theme style changes (White/Black)."""

        if not self.active:
            self._text_color_normal = (
                color
                if self.text_color_normal == [1, 1, 1, 1]
                else self.text_color_normal
            )


class MDTab(Screen, ThemableBehavior):
    """A tab is simply a screen with meta information
    that defines the content that goes in the tab header.
    """

    __events__ = (
        "on_tab_touch_down",
        "on_tab_touch_move",
        "on_tab_touch_up",
        "on_tab_press",
        "on_tab_release",
    )
    """Events provided."""

    text = StringProperty()
    """Tab header text.

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    icon = StringProperty("checkbox-blank-circle")
    """Tab header icon.

    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `'checkbox-blank-circle'`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index = 0
        self.parent_widget = None
        self.register_event_type("on_tab_touch_down")
        self.register_event_type("on_tab_touch_move")
        self.register_event_type("on_tab_touch_up")
        self.register_event_type("on_tab_press")
        self.register_event_type("on_tab_release")

    def on_tab_touch_down(self, *args):
        pass

    def on_tab_touch_move(self, *args):
        pass

    def on_tab_touch_up(self, *args):
        pass

    def on_tab_press(self, *args):
        par = self.parent_widget
        if par.previous_tab is not self:
            if par.previous_tab.index > self.index:
                par.ids.tab_manager.transition.direction = "right"
            elif par.previous_tab.index < self.index:
                par.ids.tab_manager.transition.direction = "left"
            par.ids.tab_manager.current = self.name
            par.previous_tab = self

    def on_tab_release(self, *args):
        pass

    def __repr__(self):
        return f"<MDTab name='{self.name}', text='{self.text}'>"

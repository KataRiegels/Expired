from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.bottomnavigation import MDBottomNavigationItem,MDBottomNavigationHeader
from kivymd.uix.toolbar import MDToolbar


# class MyBottomNavigationHeader(MDBottomNavigationHeader):
#     def on_press(self) -> None:
#         """Called when clicking on a panel item."""

#         if self.theme_cls.material_style == "M2":
#             Animation(_label_font_size=sp(14), d=0.1).start(self)
#         elif self.theme_cls.material_style == "M3":
#             Animation(
#                 _selected_region_width=dp(64),
#                 t="in_out_sine",
#                 d=0,
#             ).start(self)
#         Animation(
#             _text_color_normal=self.theme_cls.primary_color
#             # _text_color_normal=self.theme_cls.primary_dark_hue
#             if self.text_color_active == [1, 1, 1, 1]
#             else self.text_color_active,
#             d=0.1,
#         ).start(self)

"""
Navigation bar widget
"""
class MNavigationBar(MDBottomNavigation):
    
    def __init__(self, **kwargs):
        self.current_tab = 1
        super().__init__(**kwargs)
    
    # def on_press(self):
    #     Animation(_label_font_size=sp(14), d=0.1).start(self)
    #     Animation(
    #         _text_color_normal=self.theme_cls.primary_color,
    #         d=0.1,
    #     ).start(self)
    
    # def updateBackList(self,current):
    #     self.latest_tabs.append(current)
    #     if len(self.latest_tabs) > 4:
    #         self.latest_tabs.pop(0)
    #     return self.latest_tabs[-1]
    #     pass
    
    """ Using the "order" to get retrieve the Screen instance """
    def get_screen_from_order(self,order):
        for    tab in self.ids.tab_manager.screens:
            if tab.order == order:  return tab
        
    """ Handles which screen should be displayed based on swipe direction """    
    def swipe_screen(self, right):
        sm          = self.ids.tab_manager  
        current     = sm.current_screen
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
    
    
    """ Going back to the latest screen (or home screen when clicked twice) """
    def back_screen(self):
        to_screen_order     = self.current_tab
        to_screen           = self.get_screen_from_order(to_screen_order)
        if self.current_tab == self.ids.tab_manager.current_screen.order:
            self.switch_tab("menu")
        else: self.switch_tab(to_screen.name)
    
    """ Basic screen change when pressing navigation bar tabs """    
    def change_screen(self,to_screen):
        sm      = self.ids.tab_manager  
        current = sm.current_screen      
        if current.order < sm.get_screen(to_screen).order:   sm.transition.direction = 'left'
        if current.order > sm.get_screen(to_screen).order:   sm.transition.direction = 'right'
        self.current_tab = current.order



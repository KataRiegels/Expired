from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.bottomnavigation import MDBottomNavigationItem,MDBottomNavigationHeader
from kivymd.uix.toolbar import MDToolbar


"""
Navigation bar widget
"""
class MNavigationBar(MDBottomNavigation):
    
    def __init__(self, **kwargs):
        self.current_tab = 1
        super().__init__(**kwargs)
    
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



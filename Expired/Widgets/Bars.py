from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.toolbar import MDToolbar
from kivymd.app import MDApp



class MNavigationBar(MDBottomNavigation):
    
    def get_screen_from_order(self,order):
        # for tab in self.children:
        for tab in self.ids.tab_manager.screens:
            if tab.order == order:
                return tab.name
        pass
        
    def swipe_screen(self, right):
        sm = self.ids.tab_manager  
        current = sm.current_screen      
        if right:
            sm.transition.direction = 'right'
            if not current.order < 2:
                next_screen = self.get_screen_from_order(current.order-1)
            self.switch_tab(next_screen)
        else:
            sm.transition.direction = 'left'
            if not current.order > 3:
                next_screen = self.get_screen_from_order(current.order+1)
            self.switch_tab(next_screen)
    
    def change_screen(self,to_screen):
        sm = self.ids.tab_manager  
        current = sm.current_screen      
        if current.order < sm.get_screen(to_screen).order:
            sm.transition.direction = 'left'
        if current.order > sm.get_screen(to_screen).order:
            sm.transition.direction = 'right'
        
    pass

class NavigationItem(MDBottomNavigationItem):
    
    pass


class Toolbar(MDToolbar):
    pass
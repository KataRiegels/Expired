from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.toolbar import MDToolbar
from kivymd.app import MDApp



class MNavigationBar(MDBottomNavigation):
    
    def __init__(self, **kwargs):
        # print(self.widget_index
        # self.widget_index = 0
        
        super().__init__(**kwargs)
        # self.sm = self.ids.tab_manager
        
    def get_screen_from_order(self,order):
        # for tab in self.children:
        for tab in self.ids.tab_manager.screens:
            if tab.order == order:
                return tab.name
        pass
        
    def swipe_screen(self, right):
        # if self.enable_swipe:
            # i = int(self.sm.current)
        sm = self.ids.tab_manager  
        current = sm.current_screen      
        # if current.order < sm.get_screen(to_screen).order:
        if right:
            sm.transition.direction = 'right'
            if not current.order < 2:
                next_screen = self.get_screen_from_order(current.order-1)
            self.switch_tab(next_screen)
            # self.bar.switch_tab("list")
            # self.sm.current = str((i-1) % len(self.screens))
        else:
            sm.transition.direction = 'left'
            if not current.order > 3:
                next_screen = self.get_screen_from_order(current.order+1)
            self.switch_tab(next_screen)
            # self.sm.transition.direction = 'left'
            # self.bar.switch_tab("list")
    
    def change_screen(self,to_screen):
        sm = self.ids.tab_manager  
        current = sm.current_screen      
        if current.order < sm.get_screen(to_screen).order:
            sm.transition.direction = 'left'
        if current.order > sm.get_screen(to_screen).order:
            sm.transition.direction = 'right'
            print("dklfslkdjfslkdjfsljkf")
        # self.switch_tab(to_screen)
        
        
        
        
        # self.sm = MDApp.get_running_app().sm
        # s = self.sm.get_screen(to_screen)
        # # s.ids.bottom_nav.switch_tab(to_screen)
        # # self.switch_tab(to_screen)
        # self.sm.current = to_screen
        pass
    
    
    pass

class NavigationItem(MDBottomNavigationItem):
    
    pass


class Toolbar(MDToolbar):
    pass
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.toolbar import MDToolbar
from kivymd.app import MDApp



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

class NavigationItem(MDBottomNavigationItem):
    
    pass


class Toolbar(MDToolbar):
    pass
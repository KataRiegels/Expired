from kivy.uix.screenmanager      import Screen
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from gestures4kivy               import CommonGestures

"""
The super-class for all the screens
"""
class MyScreen(MDBottomNavigationItem,CommonGestures):
    
    """ Responsible for change of screens when swiping """
    def cg_swipe_horizontal(self, touch, right):
        self._parent.swipe_screen(right)
        
    """ For when the fridge is updated """    
    def updated_fridge(self):
        pass
        
    """ For building certain parts of a screen """
    def initiate_screen(self):
        pass
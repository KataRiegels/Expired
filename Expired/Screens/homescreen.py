

from kivymd.app                 import MDApp
from kivy.uix.relativelayout    import RelativeLayout
from .                          import MyScreen

"""
Class responsible for positioning and labelling the sticky note presented items
"""
class DateLayout(RelativeLayout):        
    def set_labels(self,item):
        self.ids.expiry_date_lbl.text = item.expiry_date.as_string()
        self.ids.product_name_lbl.text = item.product_name

class HomeScreen(MyScreen):
    
    """ Adding the next 6 expiring food items to the sticky note """
    def initiate_screen(self):
        self.ids.dates_layout.clear_widgets()
        for item in MDApp.get_running_app().fridge.sorted_fridge_list:
            food = DateLayout()
            food.set_labels(item)
            self.ids.dates_layout.add_widget(food)
            if len(self.ids.dates_layout.children)>5:
                break
            
    """ Updates the sticky note upon adding or deleting items """
    def updated_fridge(self):
        self.initiate_screen()
        




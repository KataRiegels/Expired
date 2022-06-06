
from . import MyScreen

""" List screen with interactable display of items """
class ListScreen(MyScreen):
    def __init__(self,items = None,**kwargs):
        super().__init__(**kwargs)
        self.items = items

    def initiate_screen(self):
        self.ids.select_view.create_item_list_widget()







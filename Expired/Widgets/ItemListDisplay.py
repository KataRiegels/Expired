from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.list import BaseListItem
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window
import threading
from kivymd.app import MDApp

import threading
import time
from kivy.clock import Clock, mainthread

"""Class that uses the abstract MD BaseListItem. 
Used when adding a widget to the item list
"""

""" Removable? FoodItemSelection used to inherit"""
# class ListItemBase(BaseListItem):
#     pass


""" The widget that is put into the MySelectionList"""
class FoodItemSelection(BaseListItem):
    def __init__(self,item = None, _owner = None):
        self.item = item
        self._owner = _owner
        super().__init__()
    def createOption(self):
        self.ids.list_item.exp_date_lbl = self._owner.expiryDate.toString()
        self.ids.list_item.product_name_lbl = self._owner.productName

    def __repr__(self):
        return str(self._owner.productName)

""" Holds lists of widgets - includes the list in Items and ItemViewList """
class ItemWidgetList(list):
    def __init__(self,fridge = None):
        self.fridge = fridge
        self.sorted_fridge_list = []
        self.sort_date()
    
    def sort_date(self,ascending = True):
        self.sort(reverse=not ascending, key=lambda x: (x._owner.expiryDate,x._owner.productName.casefold()))

    def sort_name(self,ascending = True):
        self.sort(reverse=not ascending, key=lambda x: (x._owner.productName.casefold(),x._owner.expiryDate))
    
    def refill_list(self,list):
        
        self.clear()
        for widget in list:
            self.append(widget)



class MSnackbar(Snackbar):
    pass

class ConfirmDelete(MDDialog):
    
    def __init__(self, _parent = None, deleted_items = None, **kwargs):
        self.cancel_button = MDFlatButton(
                text="CANCEL",
                text_color=MDApp.get_running_app().theme_cls.primary_color,
                on_release= self.dismiss,
            )
        self.ok_button = MDFlatButton(
                text="CONFIRM",
                text_color=MDApp.get_running_app().theme_cls.primary_color,
                on_release= self.confirm_button,
            )
        buttons=[
            self.cancel_button, self.ok_button
        ]
        # self.deleted_items = deleted_items
        self.findItems(deleted_items)
        super().__init__(buttons = buttons, **kwargs)
        self._parent = _parent
        
    def confirm_button(self,intsance):
        self._parent.delete_items()
        self.dismiss()

    def findItems(self,items):
        self.text = ""; noofitems = 0
        for item in items:
            noofitems += 1
            self.text += f"{item.instance_item._owner.toString()}"
            if noofitems >= 3:
                self.text += "\n..."
                break
            elif len(items) > noofitems:
                self.text += "\n"

""" The part that handles the whole list area
"""
class ItemListView(RelativeLayout):

    # list_of_items = []
    # list_of_items_sorted = []
    # current_widgets = []
    # current_widgets = []
    fridge = None

    def create_item_list_widget(self,screen=None):
        self.screen = screen
        self.fridge = MDApp.get_running_app().fridge
        self.widgets = self.fridge.widget_list
        self.selection_list = self.ids.selection_list
        self.current_widgets = ItemWidgetList()
        
        self.add_all_items()
        self.refresh_widgets()

    def add_item_to_list(self,item):
        option = item.food_item_selection
        option.createOption()
        self.current_widgets.append(option)
        self.selection_list.add_widget(option)

    # def complete_refresh(self):
    #     self.widgets = self.fridge.widget_list
    #     self.add_all_items()
    #     self.refresh_widgets()
        

    """ Not sure what this was for. Does literally nothing. """
    # def refresh_on_exit(self):
    #     # self.widgets = self.fridge.widget_list
    #     self.add_all_items()
    #     self.refresh_widgets()

    """ Adds the widgets to the MySelectionList list view widget """
    def refresh_widgets(self):
        self.selection_list.clear_widgets()
        for item in self.current_widgets:
            self.selection_list.add_widget(item)
        # print(self.selection_list.canvas.children)
            


    """Just adds all items to the list view"""
    def add_all_items(self):
        self.current_widgets.clear()
        for item in self.fridge:
            food = FoodItemSelection(_owner = item)
            food.createOption()
            self.current_widgets.append(food)

    """Sorts the list view by date"""
    def sortDate(self,ascending = True):
        self.current_widgets.sort_date(ascending=ascending)
        self.refresh_widgets()

    """Sorts the list view by name"""
    def sortName(self,ascending = True):
        self.current_widgets.sort_name(ascending=ascending)
        self.refresh_widgets()

    """Deletes the items selected by user"""
    def pressed_delete(self):
        items = self.selection_list.get_selected_list_items()
        if not items: # If the user did not select any items
            MSnackbar().open()
        else:         # Asking user to confirm delete
            delete_dialog = ConfirmDelete(_parent = self,deleted_items = items)
            delete_dialog.open()
    
    def delete_items(self):
        items = self.selection_list.get_selected_list_items()
        for item in items:
            # self.screen.manager.fridge.removeItem(item.instance_item._owner)
            MDApp.get_running_app().fridge.removeItem(item.instance_item._owner)
            self.current_widgets.remove(item.instance_item._owner.food_item_selection)
            self.selection_list.remove_widget(item)

    # def resetList(self):
    #     pass

    """ Adds back all the items to the current widgets list"""
    def refresh_list(self):
        # self.current_widgets = self.widgets.copy()
        self.current_widgets.refill_list(self.widgets)
        self.ids.toolbar.title = "Items"
        self.refresh_widgets()

    """ Checks for which items contain searched string and adds it to the list widget """
    def search_items(self,string):
        self.selection_list.clear_widgets()
        for widget in self.current_widgets.copy():
            r = widget._owner.productName.find(string)
            if r==-1:
                self.current_widgets.remove(widget)
        self.refresh_widgets()
    
    # def searchItems(self):
    #     search_input = self.ids.search_popup.ids.search_field.text
    #     # self.search_items(search_input)
    #     self.selection_list.clear_widgets()
    #     for widget in self.current_widgets.copy():
    #         r = widget._owner.productName.find(search_input)
    #         if r==-1:
    #             self.current_widgets.remove(widget)
    #     self.refresh_widgets()
        
    def open_sort_by(self):
        SortByPopup(_parent = self).open()
        self.refresh_widgets()
    
    def open_search(self):
        self.refresh_list()
        SearchPopup(_parent = self).open()


class SortByPopup(Popup):
    def __init__(self, _parent = None, **kwargs):
        super().__init__(**kwargs)
        self._parent =  _parent
    
    pass
      
class SearchPopup(ModalView):
    def __init__(self, _parent = None, **kwargs):
        super().__init__(**kwargs)
        self._parent =  _parent

    def clicked_search(self):
        search_text = self.ids.search_field.text
        self._parent.search_items(search_text)
        self._parent.ids.toolbar.title = search_text
        self.dismiss()
        pass
    
    
    
    
    
    
    
# """ Representing the expiry date of an item """
# class Date():

#     months_dict = \
#         {"1":{"full": "January",    "clipped":"Jan"},
#         "2":{ "full": "February",   "clipped":"Feb"},
#         "3":{ "full": "March",      "clipped":"Mar"},
#         "4":{ "full": "April",      "clipped":"Apr"},
#         "5":{ "full": "May",        "clipped":"May"},
#         "6":{ "full": "June",       "clipped":"Jun"},
#         "7":{ "full": "July",       "clipped":"Jul"},
#         "8":{ "full": "August",     "clipped":"Aug"},
#         "9":{ "full": "September",  "clipped":"Sep"},
#         "10":{"full": "October",    "clipped":"Oct"},
#         "11":{"full": "November",   "clipped":"Nov"},
#         "12":{"full": "December",   "clipped":"Dec"},
#     }

#     def __init__(self,day=1,month=1,year=2000):
#         self.day = day; self.month = month; self.year = year

#     """ For sorting based on date """
#     def __lt__(self,other):
#         return (self.year,self.month,self.day) < (other.year,other.month,other.day)
#     def __gt__(self,other):
#         return (self.year,self.month,self.day) > (other.year,other.month,other.day)
#     def __eq__(self,other):
#         return (self.year,self.month,self.day) == (other.year,other.month,other.day)

#     # "%02d" % (number,)
#     def toString(self):
#         return f"{self.day:02d}/{self.month:02d}-{self.year}"

#     def toString_DMY(self):
#         return f"{self.day}/{self.month}-{self.year}"
    
#     def toString_MDY(self):
#         # if self.day < 10:
#         return f"{self.month}/{self.day}-{self.year}"

#     def toString_DMY_month(self):
#         return f"{self.months_dict[str(self.month)]}"
    
    
    
    
# from random import randint
# class Item():
    
#     def __init__(self,productName = "NaN",expiryDate=Date(2000,1,1), ID = "Invalid"):
#         self.productName = productName
#         self.expiryDate  = expiryDate
#         self.ID          = ID
#         self.food_item_selection = FoodItemSelection(_owner = self)
#         self.food_item_selection.createOption()
        
#         # self.food_item_selection = None

#     """ Generates an ID for an item with 4 random digits"""
#     def createUniqueID(self):
#         ID = str(randint(1000,4999))
#         self.ID = self.productName + ID

#     """ Arranges the information so it can be stored in the JSON file """
#     def convertToJSONInput(self):
#         return [self.productName,[self.expiryDate.year,self.expiryDate.month,self.expiryDate.day]]

#     """ In order for displaying the item """
#     def toString(self):
#         return f"{self.productName} expiring {self.expiryDate.toString()}"









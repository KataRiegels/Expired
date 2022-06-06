from kivymd.uix.relativelayout  import RelativeLayout
from kivymd.uix.list            import BaseListItem
from kivymd.uix.snackbar        import Snackbar
from kivymd.uix.dialog          import MDDialog
from kivy.uix.popup             import Popup
from kivy.uix.modalview         import ModalView
from kivymd.uix.button          import MDFlatButton
from kivymd.app                 import MDApp



# --------------------------------------------------------- #
# ----------- INTERACTABLE DISPLAY OF ITEMS --------------- #
# --------------------------------------------------------- #

""" 
The class that handles the interactions for the interactable display of items
"""
class ItemListView(RelativeLayout):
    fridge = None

    """ Initial creation of the widget - loads and creates lists all saved items """
    def create_item_list_widget(self):
        self.fridge          = MDApp.get_running_app().fridge   # The fridge instance of the Items class
        self.widgets         = self.fridge.widget_list          # The list of FoodSelectionItems from Items instance
        self.selection_list  = self.ids.selection_list          # The MySelectionList widget instance
        self.current_widgets = ItemWidgetList()                 # The list of widgets used for manipulating only currently displayed items 
        self.add_all_items()
        self.refresh_widgets()

            
    """ Adds all items to the list view"""
    def add_all_items(self):
        self.current_widgets.clear()
        for item in self.fridge:
            food = item.food_item_selection
            food.createOption()
            self.current_widgets.append(food)
            
    """ Adds a single item to the item display """
    def add_item_to_list(self,item):
        option = item.food_item_selection
        option.createOption()
        self.current_widgets.append(option)
        self.selection_list.add_widget(option)

    """ Adds the widgets to the MySelectionList widget """
    def refresh_widgets(self):
        self.selection_list.clear_widgets()
        for item in self.current_widgets:
            self.selection_list.add_widget(item)


    # --------- For deleting items ---------------
    
    """ When user presses the delete button - triggers either snackbar or deletion """
    def pressed_delete(self):
        items = self.selection_list.get_selected_list_items()
        if not items: # If the user did not select any items
            MSnackbar().open()
        else:         # Asking user to confirm delete
            delete_dialog = ConfirmDelete(_parent = self,deleted_items = items)
            delete_dialog.open()
    
    """ Removes the items from all lists/widgets  """
    def delete_items(self):
        items = self.selection_list.get_selected_list_items()
        for item in items:
            self.current_widgets.remove(item.instance_item._owner.food_item_selection)
            MDApp.get_running_app().fridge.remove_item_from_fridge(item.instance_item._owner)
            self.selection_list.remove_widget(item)


    # --------- For searching through items ------------ 
    
    """ Opens popup for searching in the item display """
    def open_search(self):
        self.refresh_list()
        SearchPopup(_parent = self).open()

    """ Adds back all the items to the current_widgets list"""
    def refresh_list(self):
        self.current_widgets.refill_list(self.widgets)
        self.ids.toolbar.title = "Items"
        self.refresh_widgets()

    """ Checks for which items contain searched string and adds it to the list widget """
    def search_items(self,string):
        self.selection_list.clear_widgets()
        for widget in self.current_widgets.copy():
            if_found = widget._owner.product_name.find(string) # .find() returns -1 when input wasn't detected
            if if_found==-1: 
                self.current_widgets.remove(widget)
        self.refresh_widgets()
        
        
    # -------------- For sorting items  -------------- #
    
    """ Opens popup for sorting item display """
    def open_sort_by(self):
        SortByPopup(_parent = self).open()
        self.refresh_widgets()
    
    """Sorts the list view by date"""
    def sort_display_by_date(self,ascending = True):
        self.current_widgets.sort_by_date(ascending=ascending)
        self.refresh_widgets()

    """Sorts the list view by name"""
    def sort_display_by_name(self,ascending = True):
        self.current_widgets.sort_by_name(ascending=ascending)
        self.refresh_widgets()


# --------------------------------------------------------- #
# --------------- POP-UPS --------------------------------- #
# --------------------------------------------------------- #


"""
Popup for searching within items
"""
class SortByPopup(Popup):
    def __init__(self, _parent = None, **kwargs):
        super().__init__(**kwargs)
        self._parent =  _parent

"""
Popup with buttons to sort the display of items
"""
class SearchPopup(ModalView):
    def __init__(self, _parent = None, **kwargs):
        super().__init__(**kwargs)
        self._parent =  _parent

    """ Triggers search for given input string """
    def clicked_search(self):
        search_text = self.ids.search_field.text
        self._parent.search_items(search_text)
        self._parent.ids.toolbar.title = search_text
        self.dismiss()



"""
Confirmation dialog for when user wants to delete selected items  
"""
class ConfirmDelete(MDDialog):
    
    def __init__(self, _parent = None, deleted_items = None, **kwargs):
        self.cancel_button = MDFlatButton(
                text        = "CANCEL",
                text_color  = MDApp.get_running_app().theme_cls.primary_color,
                on_release  = self.dismiss,
            )
        self.ok_button = MDFlatButton(
                text        = "CONFIRM",
                text_color  = MDApp.get_running_app().theme_cls.primary_color,
                on_release  = self.confirm,
            )
        buttons=[
            self.cancel_button, self.ok_button
        ]
        self.add_item_to_dialog(deleted_items)
        super().__init__(buttons = buttons, **kwargs)
        self._parent = _parent
        
    def confirm(self,intsance):
        self._parent.delete_items()
        self.dismiss()

    """ Adds up to three of the selected-for-delete items to display on dialog """
    def add_item_to_dialog(self,items):
        self.text = ""; noofitems = 0
        for item in items:
            noofitems += 1
            self.text += f"{item.instance_item._owner.as_string()}"
            if   noofitems >= 3:           self.text += "\n...";     break
            elif len(items) > noofitems:   self.text += "\n"

class MSnackbar(Snackbar):
    pass



# --------------------------------------------------------- #
# -------- WIDGET RELATED THINGS FOR LIST DISPLAY --------- #
# --------------------------------------------------------- #

""" 
The widget that is put into the MySelectionList
"""

class FoodItemSelection(BaseListItem):
    
    def __init__(self,item = None, _owner = None):
        self.item = item
        self._owner = _owner
        super().__init__()
        
    def createOption(self):
        self.ids.list_item.exp_date_lbl = self._owner.expiry_date.as_string()
        self.ids.list_item.product_name_lbl = self._owner.product_name

    def __repr__(self):
        return str(self._owner.product_name)


""" 
Holds lists of widgets - includes the list in Items and ItemViewList 
"""

class ItemWidgetList(list):
    def __init__(self):
        self.sort_by_date()
    
    def sort_by_date(self,ascending = True):
        self.sort(reverse=not ascending, key=lambda x: (x._owner.expiry_date,x._owner.product_name.casefold()))

    def sort_by_name(self,ascending = True):
        self.sort(reverse=not ascending, key=lambda x: (x._owner.product_name.casefold(),x._owner.expiry_date))
    
    """ Meant to copy a list without changing to "list" type """
    def refill_list(self,list):
        self.clear()
        for widget in list:     self.append(widget)



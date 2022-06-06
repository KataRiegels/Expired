from widgets.item_display import ItemWidgetList
from .                    import Date,Item
from kivymd.app           import MDApp
import json


class Items():


    def __init__(self,jsonfile = "NaN"):
        self.fridge              = {}               # Dictionary form
        self.sorted_fridge_list  = []               # List forms
        self.widget_list         = ItemWidgetList() # List for an Item's FoodSelectionItem 
        self.jsonfile            = jsonfile         # File name for stored items
        self.json_dict           = None             # Dictionary of items but in the format for a JSON file
        self.load_JSON()

    def __iter__(self):
        for key,item in self.fridge.items(): yield item

    """ Saves an item to the current lists and to the JSON file """
    def add_item_to_fridge(self,item):
        item.create_unique_ID()
        while item.ID in self.fridge.keys(): # To make sure no two products have the same ID
            item.create_unique_ID()
        self.add_item_to_lists(item)
        self.convert_to_JSON()
        self.write_to_json_file()
        MDApp.get_running_app().update_fridge()

    """ Deletes item from lists and JSON file """
    def remove_item_from_fridge(self, item):
        self.fridge.pop(item.ID)
        self.widget_list.remove(item.food_item_selection)
        self.sorted_fridge_list.remove(item)
        self.json_dict.pop(item.ID)
        self.convert_to_JSON()
        self.write_to_json_file()
        self.sort_ascending_date()
        MDApp.get_running_app().update_fridge()

    """ Adds items to the current lists and dictionaries specifically"""
    def add_item_to_lists(self,item):
        self.fridge[item.ID]   = item
        self.sorted_fridge_list.append(item)
        self.widget_list.append(item.food_item_selection)
        self.sort_ascending_date()

    """ The method called outside to load the JSON file into the current run time """
    def open_fridge(self):
        self.load_JSON()
        for key,value in self.json_dict.items():
            item  = Item(value[0],Date(year = value[1][0],month = value[1][1],day = value[1][2]),key)
            self.add_item_to_lists(item)

    """ Adds an item to the json dictionary with the format accepted by json files """
    def convert_to_JSON(self):
        for item in self.fridge.values():
            self.json_dict[item.ID] = item.as_JSON_format()

    """ Rewrites the current json file with the current json dictionary"""
    def write_to_json_file(self):
        with open(self.jsonfile, 'w') as f:
            json.dump(self.json_dict,f)

    """ Loads the JSON file and saves it in the json dict format """
    def load_JSON(self):
        file           = json.load(open(self.jsonfile))
        self.json_dict = file

    """ Sorting the sorted lists for after adding items """
    def sort_ascending_date(self):    
        self.sorted_fridge_list = sorted(self.sorted_fridge_list, key=lambda x: (x.expiry_date,x.product_name.casefold()))
        self.widget_list.sort_by_date()


    def as_string(self):
        strs = ""
        for item in self.fridge.values():
            strs = f"{strs + item.as_string()}\n"
        return strs


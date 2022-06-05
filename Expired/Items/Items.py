from widgets.item_display import ItemWidgetList
from kivymd.app import MDApp
from . import Date
from . import Item
import json
# import os


class Items():


    def __init__(self,jsonfile = "NaN"):
        self.fridge = {}
        self.sorted_fridge_list = []
        # self.sortedFridgeListName = []
        # self.widget_list = []
        self.widget_list = ItemWidgetList()
        self.jsonfile = jsonfile
        self.json_dict = None # Dictionary of items but in the format for a JSON file
        self.load_JSON()

    def __iter__(self):
        for key,item in self.fridge.items():
            yield item

    """ Saves an item to the current lists and to the JSON file """
    def add_item_to_fridge(self,item):
        item.create_unique_ID()
        while item.ID in self.fridge.keys():
            item.create_unique_ID()
        self.add_item_to_lists(item)
        self.convert_to_JSON()
        self.write_to_json_file()
        MDApp.get_running_app().update_fridge()

    """ Adds items to the current lists and dictionaries"""
    def add_item_to_lists(self,item:Item):
        self.fridge[item.ID] = item
        self.sorted_fridge_list.append(item)
        self.widget_list.append(item.food_item_selection)
        self.sort_ascending_date()
        # self.sortproduct_name()

    """ Deletes item from lists and JSON file """
    def remove_item(self, item):
        # print(type(itemID))
        print(type(item))
        self.fridge.pop(item.ID)
        self.widget_list.remove(item.food_item_selection)
        self.sorted_fridge_list.remove(item)
        self.json_dict.pop(item.ID)
        self.convert_to_JSON()
        self.write_to_json_file()
        self.sort_ascending_date()
        MDApp.get_running_app().update_fridge()

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
        # f = open(self.jsonfile)
        file = json.load(open(self.jsonfile))
        self.json_dict = file
        # return q

    """ The method called outside to load the JSON file into the current running time """
    def openFridge(self):
        self.jsonFormatToItemFormat()

    """ Takes the json dict and formats it into Item format """
    def jsonFormatToItemFormat(self,jsonitem = None):
        self.load_JSON()
        for key,value in self.json_dict.items():
            item  = Item(value[0],Date(year = value[1][0],month = value[1][1],day = value[1][2]),key)
            self.add_item_to_lists(item)
            pass

    """ Sorting the sorted lists for after adding items """
    def sort_ascending_date(self):    
        self.sorted_fridge_list = sorted(self.sorted_fridge_list, key=lambda x: (x.expiry_date,x.product_name.casefold()))
        self.widget_list.sort_date()

    def as_string(self):
        strs = ""
        for item in self.fridge.values():
            strs = f"{strs + item.as_string()}\n"
        return strs

    # """ Probably unnecessary - depends on where we want to store out data"""
    # def write_to_json_filerel(self):
    #     cur_path = os.path.dirname(__file__)
    #     new_path = os.path.relpath('..\\Data\\data.json', cur_path)

    #     with open(new_path, 'w') as f:
    #         json.dump(self.json_dict,f)

    # def load_JSONrel(self):
    #     cur_path = os.path.dirname(__file__)
    #     new_path = os.path.relpath('..\\Data\\' + self.jsonfile, cur_path)

    #     with open(new_path, 'r') as f:
    #         q = json.loads(f.read())
    #         return q


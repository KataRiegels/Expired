from widgets.item_display import FoodItemSelection
from .                    import Date
from random               import randint


"""
Food item class
"""
class Item():
    
    def __init__(self, product_name = "NaN",expiry_date=Date(2000,1,1), ID = "Invalid"):
        self.product_name        = product_name
        self.expiry_date         = expiry_date
        self.ID                  = ID
        self.food_item_selection = FoodItemSelection(_owner = self)
        self.food_item_selection.createOption()

    """ Generates an ID for an item with 4 random digits"""
    def create_unique_ID(self):
        ID_number  = str(randint(1000,4999))
        self.ID    = self.product_name + ID_number

    """ Arranges the information so it can be stored in the JSON file """
    def as_JSON_format(self):
        return [self.product_name,[self.expiry_date.year,self.expiry_date.month,self.expiry_date.day]]

    """ In order to display the item text """
    def as_string(self):
        return f"{self.product_name} expiring {self.expiry_date.as_string()}"











    






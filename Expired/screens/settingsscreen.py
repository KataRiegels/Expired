from kivy.utils              import platform
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button       import MDFillRoundFlatButton
from kivymd.uix.picker       import MDThemePicker
from kivymd.app              import MDApp
from .                       import MyScreen
import csv

"""
Settings screen class
"""
class SettingsScreen(MyScreen):
    
    """ For making API test buttons appear """
    def enable_features(self):
        self.ids.features
        # If test feeature are NOT enabled
        if self.ids.features.text == "Enable test features":
            self.ids.label_text.text = "API response" 
            self.ids.features.text   = "Disable test features"
            self.api_test = MDFillRoundFlatButton(text= 'Test cat fact API',
                    size_hint = (.5,.1),
                    pos_hint  = {'x':.25,'y':.4},
                    on_press  = self.apisaved_date)
            self.add_widget(self.api_test)
        # If test feature ARE enabled
        elif self.ids.features.text == "Disable test features":
            self.ids.label_text.text = "" 
            self.ids.features.text   = "Enable test features"
            self.remove_widget(self.api_test)
    
    """ For opening the theme picker widget """
    def show_theme_picker(self):
        theme_dialog = MDThemePicker(on_pre_dismiss = self.save_theme)
        theme_dialog.open()  
    
    """ Saving picked theme to theme.csv file so it is remembered """
    def save_theme(self,instance):
        app_theme = MDApp.get_running_app().theme_cls
        with open('save_files/theme.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow([app_theme.primary_palette,app_theme.theme_style])
    
    """ Requesting cat fact API response """        
    def apisaved_date(self,instances):
        UrlRequest("https://catfact.ninja/fact", on_success=self.get_data)

    """ Displaying cat fact """
    def get_data(self,request,response):
        self.ids.label_text.text = response['fact']
    
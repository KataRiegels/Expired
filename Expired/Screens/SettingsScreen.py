from kivy.uix.screenmanager import Screen
from . import MyScreen
from kivy.utils import platform
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import Button
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
import csv

class SettingsScreen(MyScreen):

    
    def enable_features(self):
        self.ids.features
        if self.ids.features.text == "Enable test features":
            self.ids.label_text.text = "API response" 
            self.ids.features.text = "Disable test features"
            self.api2 = MDFillRoundFlatButton(text= 'test cat api',
                    size_hint=(.5,.1),
                    pos_hint= {'x':.25,'y':.4},
                    on_press= self.apisaved_date)
            self.add_widget(self.api2)
            self.api1 = MDFillRoundFlatButton(text= 'test cat api (PC)',
                    size_hint=(.5,.1),
                    pos_hint= {'x':.25,'y':.3},
                    on_press= self.apiTEST1)
            self.add_widget(self.api1)
        elif self.ids.features.text == "Disable test features":
            self.ids.label_text.text = "" 
            self.ids.features.text = "Enable test features"
            self.remove_widget(self.api1)
            self.remove_widget(self.api2)
            
    def show_theme_picker(self):
        theme_dialog = MDThemePicker(on_pre_dismiss = self.save_theme)
        theme_dialog.open()  
        print(f"Theme is: {MDApp.get_running_app().theme_cls.primary_palette}")
            
    def save_theme(self,instance):
        app_theme = MDApp.get_running_app().theme_cls
        with open('save_files/theme.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow([app_theme.primary_palette,app_theme.theme_style])
        pass
            
    def apisaved_date(self,instances):
        request = UrlRequest("https://catfact.ninja/fact", on_success=self.get_data)

    def get_data(self,request,response):
        self.ids.label_text.text = response['fact']
    
    def apiTEST1(self):
        pass
    pass
"""
if platform == ('win'):
    from textractcaller import call_textract
    import os
    from trp import Document

class SettingsScreen(MyScreen):
    
    def apiTEST(self):

        if platform == "win":
            SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
            input_file = os.path.join(SCRIPT_DIR, "testdate2.png")
            with open(input_file, "rb") as sample_file:
                b = bytearray(sample_file.read())
                j = call_textract(input_document=b)
                assert j
                doc = Document(j)
                assert doc
                print(doc)
    

    def apisaved_date(self):
        request = UrlRequest("https://catfact.ninja/fact", on_success=self.get_data)

    def get_data(self,request,response):
        self.ids.label_text.text = response['fact']
"""
from kivy.uix.screenmanager import Screen
from . import MyScreen
from kivy.utils import platform
from kivy.network.urlrequest import UrlRequest
from kivy.uix.button import Button
from kivymd.uix.button import MDRaisedButton

class SettingsScreen(MyScreen):
    
    def enable_features(self):
        self.ids.features
        if self.ids.features.text == "enable":
            self.ids.labelText.text = "API response" 
            self.ids.features.text = "disable"
            self.api2 = MDRaisedButton(text= 'test cat api',
                    size_hint=(.5,.1),
                    pos_hint= {'x':.25,'y':.4},
                    on_press= self.apiTEST2)
            self.add_widget(self.api2)
            self.api1 = MDRaisedButton(text= 'test cat api (PC)',
                    size_hint=(.5,.1),
                    pos_hint= {'x':.25,'y':.3},
                    on_press= self.apiTEST1)
            self.add_widget(self.api1)
        elif self.ids.features.text == "disable":
            self.ids.labelText.text = "" 
            self.ids.features.text = "enable"
            self.remove_widget(self.api1)
            self.remove_widget(self.api2)
            
    def apiTEST2(self,instances):
        request = UrlRequest("https://catfact.ninja/fact", on_success=self.get_data)

    def get_data(self,request,response):
        self.ids.labelText.text = response['fact']
    
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
    

    def apiTEST2(self):
        request = UrlRequest("https://catfact.ninja/fact", on_success=self.get_data)

    def get_data(self,request,response):
        self.ids.labelText.text = response['fact']
"""
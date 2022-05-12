from functools import partial
import time
from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from . import MyScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from Items import *
from camera4kivy import Preview
from kivy.utils import platform
# from Widgets.ItemListDisplay import MSnackbar
from Widgets.ItemListDisplay import MSnackbar

if platform == 'android':
    from android.permissions import request_permissions,Permission
    from android import api_version
from kivymd.uix.button import MDRaisedButton
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp

class FilteredInput(MDTextField):
    def insert_text(self, substring, from_undo=False):
        test = ["\"", "\\", "\'"]
        for i in range(len(test)):
            if substring == test[i]:
                s = ""
                break
            else:
                s = substring
        return super().insert_text(s, from_undo=from_undo)
    def on_disabled(self, *args):
        pass

class ScanScreen(MyScreen):
    dialog = None
    selected_date = ObjectProperty(None)
    pressed_ok = ObjectProperty(None)
    itemTextInput = ObjectProperty(None)


    def test(self, value):
        self.pressed_ok.active = False
        self.ids.date_label.text = str(self.test2)

    def on_save(self, instance, value, date_range):
        self.pressed_ok.active = True
        self.test2 = value
        print("ON_SAVE WAS CALLLLEEEDDD")
        
        Clock.schedule_once(self.test,1)
        # self.save_item_to_fridge(self.test2)

    def on_pre_enter(self):
        # self.selected_date.text ="Select a Date"
        self.test2 = None

        if platform == 'android':
            permissions = [Permission.CAMERA, Permission.RECORD_AUDIO]
            if api_version < 29:
                permissions.append(Permission.WRITE_EXTERNAL_STORAGE)        
            request_permissions(permissions)
        self.ids.preview.connect_camera()

    def on_leave(self):
        self.ids.preview.disconnect_camera()

    def photo(self):
        self.ids.preview.capture_photo()
        Clock.schedule_once(self.test, 0.5)

    def save_item(self):
        if self.itemTextInput.text == "":
            # MSnackbar().open()
            save_item_warning = MSnackbar()
            save_item_warning.text = "Please enter a product name first"    
            save_item_warning.open()
        elif not self.test2:
            # MSnackbar().open()
            save_item_warning = MSnackbar()
            save_item_warning.text = "Please pick a date first"    
            save_item_warning.open()
        # if self.itemTextInput.text == "":
        #     self.dialog = MDDialog(
        #         text="Please enter an item name",
        #         radius=[20, 7, 20, 7],
        #         buttons=[
        #             MDFlatButton(
        #                 text="CLOSE",
        #                 on_release = self.close_dialog
        #             ),
        #         ],
        #     )
        # elif not self.test2:
        #     self.dialog = MDDialog(
        #         text="Please select a date",
        #         radius=[20, 7, 20, 7],
        #         buttons=[
        #             MDFlatButton(
        #                 text="CLOSE",
        #                 on_release = self.close_dialog
        #             ),
        #         ],
        #     )
        else:
            self.dialog = MDDialog(
                text=self.itemTextInput.text[:5] + " expires on " +
                str(self.test2.day) + " " + str(self.test2.month) +
                " " + str(self.test2.year),
                radius=[20, 7, 20, 7],
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release = self.close_dialog
                    ),
                    MDRaisedButton(
                        text="CONFIRM",
                        on_release = self.onConfirm
                    ),
                ],
            )
            self.dialog.open()

    def on_cancel(self, instance, value):
        pass

    def close_dialog(self, instance):
        if self.dialog:
            self.dialog.dismiss()

    def onConfirm(self,instance):
        self.save_item_to_fridge(self)
        self.ids.date_label.text = "Select a Date"
        self.ids.itemName.text = ""
        self.close_dialog(self)


    def show_date_picker(self):
        # date_dialog = MDDatePicker(md_bg_color = MDApp.get_running_app().theme_cls.primary_light)
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


    # Katas work:
    def save_item_to_fridge(self,item_save = None):
        item_save = self.test2
        productName = self.itemTextInput.text
        expDate = Date(year = item_save.year,month = item_save.month, day=item_save.day)
        item = Item(productName,expDate)
        app = MDApp.get_running_app()
        app.fridge.addItemToFridge(item)
        # manager = app.bar
        # list_screen = manager.ids.list_tab
        app.list_screen.ids.select_view.onLateEnter()
        

        # text = self.itemTextInput.text + " expires on " + str(self.test2.day) +" "+ str(self.test2.month) +" "+ str(self.test2.year),

    

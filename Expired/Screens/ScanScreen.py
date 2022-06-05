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
from kivymd.uix.textfield import MDTextField, MDTextFieldRound
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
    # def on_disabled(self, *args):
    #     pass

class ScanScreen(MyScreen):
    dialog = None
    selected_date = ObjectProperty(None)
    spinner = ObjectProperty(None)
    itemTextInput = ObjectProperty(None)


    """ Stops the spinner after picked date """
    def stopSpinner(self, value):
        self.spinner.active = False
        self.ids.date_label.text = self.current_date.toString()

    """ Triggered when clicking "Confirm" at the date pickers
    Saving the date  """
    def on_save(self, instance, value, date_range):
        self.spinner.active = True
        self.current_date = Date(year =value.year,month = value.month, day=value.day)
        self.saved_date = value
        Clock.schedule_once(self.stopSpinner,1)

    """ Asking for permission as screen is created """
    def initiateScreen(self):
        if platform == 'android':
            permissions = [Permission.CAMERA, Permission.RECORD_AUDIO]
            if api_version < 29:
                permissions.append(Permission.WRITE_EXTERNAL_STORAGE)        
            request_permissions(permissions)
        
        return super().initiateScreen()

    """ Method called by Kivy as screen is entered
    Connects the camera """
    def on_enter(self):
        self.saved_date = None
        self.ids.preview.connect_camera()

    """ Disconnecting camera when leaving scan screen """
    def on_pre_leave(self):
        self.ids.preview.disconnect_camera()

    """ Captures a photo to use for OCR """
    def photo(self):
        self.ids.preview.capture_photo()
        Clock.schedule_once(self.stopSpinner, 0.5)

    """ When pressing the "Save item" button
    Either adds the item to the fridge or displays snackbars """
    def save_item(self):
        if self.itemTextInput.text == "": # If product name was not given
            save_item_warning = MSnackbar()
            save_item_warning.text = "Please enter a product name first"    
            save_item_warning.open()
        elif not self.saved_date:         # If date was not given 
            save_item_warning = MSnackbar()
            save_item_warning.text = "Please pick a date first"    
            save_item_warning.open()
        else:
            date  = Date(year =self.saved_date.year,month = self.saved_date.month, day=self.saved_date.day)
            dialog_text = f"{date.toString()}     {self.itemTextInput.text}"
            dialog = ConfirmAdd(self, text = dialog_text)
            dialog.text = dialog_text
            dialog.open()

    # def on_cancel(self, instance, value):
    #     pass

    # def close_dialog(self, instance):
        
    #     # if self.dialog:
    #     self.dialog.dismiss()

    """ When confirming saved item 
    Calls for saving item and 'refreshes' entered info """
    def on_confirm(self,instance):
        self.save_item_to_fridge(self)
        self.ids.date_label.text = "Select a Date"
        self.ids.itemName.text = ""
        # self.dialog.dismiss()
        # self.close_dialog(self)

    """ Open date picker """
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        # date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    """ Creates the actual item and adds it to the Items instance """
    def save_item_to_fridge(self,item_save = None):
        item_save = self.saved_date
        productName = self.itemTextInput.text
        expDate = Date(year = item_save.year,month = item_save.month, day=item_save.day)
        item = Item(productName,expDate)
        app = MDApp.get_running_app()
        app.fridge.add_item_to_fridge(item)
        app.list_screen.ids.select_view.add_item_to_list(item)
        # app.list_screen.ids.select_view.complete_refresh()
        # app.list_screen.ids.select_view.initialEnter()
        

""" Confirm dialog when saving an item """
class ConfirmAdd(MDDialog):
    """ Add confirm and cancel buttons to the dialog """
    def __init__(self, _parent = None, **kwargs):
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
        buttons=[self.cancel_button, self.ok_button]
        # self.deleted_items = deleted_items
        # self.findItems(deleted_items)
        super().__init__(buttons = buttons, **kwargs)
        self._parent = _parent # Such that the scan screen can be accessed
    
    """ When confirm button on dialog is pressed """
    def confirm_button(self,instance):
        self.dismiss()
        # Clock.schedule_once(self._parent.on_confirm,.2)
        self._parent.on_confirm(instance)

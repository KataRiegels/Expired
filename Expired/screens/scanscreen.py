from kivymd.uix.picker      import MDDatePicker
from kivymd.uix.dialog      import MDDialog
from kivymd.uix.button      import MDFlatButton
from kivy.properties        import ObjectProperty
from kivy.clock             import Clock
from .                      import MyScreen
from items                  import Date,Item
from widgets.item_display   import MSnackbar
from camera4kivy            import Preview
from kivy.utils             import platform
if platform == 'android':
    from android.permissions import request_permissions,Permission
    from android import api_version
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp

import datetime

""" 
Scan screen class
"""
class ScanScreen(MyScreen):
    dialog          = None
    selected_date   = ObjectProperty(None)
    spinner         = ObjectProperty(None)
    item_text_input = ObjectProperty(None)


    """ Stops the spinner after picked date """
    def stop_spinner(self, value):
        self.spinner.active = False
        self.ids.date_picker_button.text = self.current_date.as_string()

    """ Triggered when clicking "Confirm" at the date pickers
    Saving the date  """
    def on_save(self, instance, value, date_range):
        self.spinner.active = True
        self.current_date   = Date(year =value.year,month = value.month, day=value.day)
        self.saved_date     = value
        Clock.schedule_once(self.stop_spinner,.6)

    """ Asking for permission as screen is created """
    def initiate_screen(self):
        if platform == 'android':
            # permissions = [Permission.CAMERA, Permission.RECORD_AUDIO]
            permissions = [Permission.CAMERA]
            if api_version < 29:
                permissions.append(Permission.WRITE_EXTERNAL_STORAGE)        
            request_permissions(permissions)
        return super().initiate_screen()

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
        # Clock.schedule_once(self.stop_spinner, 0.5)

    """ When pressing the "Save item" button
    Either adds the item to the fridge or displays snackbars """
    def save_item(self):
        if self.item_text_input.text == "": # If product name was not given
            save_item_warning = MSnackbar()
            save_item_warning.text = "Please enter a product name first"    
            save_item_warning.open()
        elif not self.saved_date:         # If date was not given 
            save_item_warning = MSnackbar()
            save_item_warning.text = "Please pick a date first"    
            save_item_warning.open()
        else:
            date        = Date(year =self.saved_date.year,month = self.saved_date.month, day=self.saved_date.day)
            dialog_text = f"{date.as_string()}     {self.item_text_input.text}"
            dialog      = ConfirmAdd(self, text = dialog_text)
            dialog.text = dialog_text
            dialog.open()


    """ When confirming saved item 
    Calls for saving item and 'refreshes' entered info """
    def on_confirm(self,instance):
        self.save_item_to_fridge()
        self.ids.date_picker_button.text = "Select a Date"
        self.ids.product_name_input.text = ""

    """ Open date picker """
    def show_date_picker(self):
        # min_date = datetime.strptime("2022:01:01", '%Y:%m:%d').date()
        # min_date = Date(2022,1,1)
        date_dialog = MDDatePicker(min_year=2022)
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    """ Creates the actual item and adds it to the Items instance """
    def save_item_to_fridge(self):
        item_save       = self.saved_date
        product_name    = self.item_text_input.text
        expiry_date     = Date(year = item_save.year,month = item_save.month, day=item_save.day)
        item            = Item(product_name,expiry_date)
        app             = MDApp.get_running_app()
        app.fridge.add_item_to_fridge(item)
        app.list_screen.ids.select_view.add_item_to_list(item)
        
"""
The input field for product name
"""
class FilteredInput(MDTextField):
    def insert_text(self, substring, from_undo=False):
        filtered_characters = ["\"", "\\", "\'"]
        for character in filtered_characters:
            if substring == character:
                s = ""
                break
            else:
                s = substring
        return super().insert_text(s, from_undo=from_undo)

""" 
Confirm dialog when saving an item 
"""
class ConfirmAdd(MDDialog):
    """ Add confirm and cancel buttons to the dialog """
    def __init__(self, _parent = None, **kwargs):
        self.cancel_button = MDFlatButton(
                text        = "CANCEL",
                text_color  = MDApp.get_running_app().theme_cls.primary_color,
                on_release  = self.dismiss,
            )
        self.ok_button = MDFlatButton(
                text        = "CONFIRM",
                text_color  = MDApp.get_running_app().theme_cls.primary_color,
                on_release  = self.confirm_button,
            )
        buttons=[self.cancel_button, self.ok_button]
        super().__init__(buttons = buttons, **kwargs)
        self._parent = _parent # Such that the scan screen can be accessed
    
    """ When confirm button on dialog is pressed """
    def confirm_button(self,instance):
        self.dismiss()
        self._parent.on_confirm(instance)

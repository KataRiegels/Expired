


from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import TouchBehavior

from kivymd.uix.button import MDIconButton
from kivymd.uix.list import MDList
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.selection import SelectionItem
from kivymd.uix.selection import SelectionIconCheck

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import (
    Ellipse,
    RoundedRectangle,
    SmoothLine,
)
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.animation import Animation
from kivy.clock import Clock


class MySelectionItem(SelectionItem):
    def on__progress_animation(self, instance, value):
        if value:
            anim = Animation(_progress_line_end=360, d=.3, t="in_out_quad")
            anim.bind(
                on_progress=self.do_animation_progress_line,
                on_complete=self.do_selected_item,
            )
            anim.start(self)
            self._instance_progress_inner_outer_color.rgba = (
                self.get_progress_line_color()
            )
            self._instance_progress_inner_circle_color.rgba = (
                self.get_progress_round_color()
            )
        else:
            self.reset_progress_animation()


class MySelectionList(MDList):
    selected_mode = BooleanProperty(False)
    icon = StringProperty("check")
    icon_pos = ListProperty()
    icon_bg_color = ColorProperty([1, 1, 1, 1])
    icon_check_color = ColorProperty([0, 0, 0, 1])
    overlay_color = ColorProperty([0, 0, 0, 0.2])
    progress_round_size = NumericProperty(dp(46))
    progress_round_color = ColorProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_selected")
        self.register_event_type("on_unselected")

    def add_widget(self, widget, index=0, canvas=None):
        selection_icon = SelectionIconCheck(
            icon=self.icon,
            md_bg_color=self.icon_bg_color,
            icon_check_color=self.icon_check_color,
        )
        widget.parent = None
        container = MySelectionItem(
            size_hint=(1, None),
            height=widget.height,
            instance_item=widget,
            instance_icon=selection_icon,
            overlay_color=self.overlay_color,
            progress_round_size=self.progress_round_size,
            progress_round_color=self.progress_round_color,
            owner=self,
        )
        container.add_widget(widget)
        if not self.icon_pos:
            pos = (
                dp(12),
                container.height / 2 - selection_icon.height / 2,
            )
        else:
            pos = self.icon_pos
        selection_icon.pos = pos
        return super().add_widget(container, index, canvas)

    def get_selected(self) -> bool:
        selected = False
        for item in self.children:
            if item.selected:
                selected = True
                break
        return selected

    def get_selected_list_items(self) -> list:
        selected_list_items = []
        for item in self.children:
            if item.selected:
                selected_list_items.append(item)
        return selected_list_items

    def unselected_all(self) -> None:
        for item in self.children:
            item.do_unselected_item()
        self.selected_mode = False

    def selected_all(self) -> None:
        for item in self.children:
            item.do_selected_item()
        self.selected_mode = True

    def on_selected(self, *args):
        if not self.selected_mode:
            self.selected_mode = True

    def on_unselected(self, *args):
        self.selected_mode = self.get_selected()

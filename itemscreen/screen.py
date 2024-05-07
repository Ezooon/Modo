from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ColorProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar

Builder.load_file("itemscreen/ui.kv")


class ItemScreenToolBar(MDTopAppBar):
    screen = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Item"
        self.left_action_items = [["arrow-left", self.on_back]]
        self.right_action_items = [["heart-outline", self.screen.add_to_favorite]]

    def on_back(self, *args):
        self.screen.parent.current = "home"


class ItemScreen(MDScreen):
    item = ObjectProperty()
    description = StringProperty("")
    price = NumericProperty(1)
    image = StringProperty("assets/item.jpg")
    stock = NumericProperty(1)
    cart_units = NumericProperty(1)
    background_color = ColorProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.toolbar = None

    # def on_ids(self, _, ids):
    #     self.toolbar = ItemScreenToolBar(screen=self)
    #     self.ids.appbar.toolbar_cls = self.toolbar

    def add_to_favorite(self, _):
        from utils.image_colors import get_accent_color
        color = get_accent_color(self.ids.image._container.image)
        _.md_bg_color = color
        self.background_color = color

    def on_item(self, _, item):
        from utils.image_colors import get_accent_color
        self.cart_units = 0
        self.ids.title.text = item.name
        self.description = item.description
        self.price = item.price
        self.image = item.image
        if self.image:
            color = get_accent_color(self.ids.image._container.image)
            self.background_color = color
        self.stock = item.stock


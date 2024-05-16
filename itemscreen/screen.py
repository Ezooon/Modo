from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ColorProperty

from api.item import Item
from kivymd.toast import toast

from utils.image_colors import get_accent_color

from api.cart import CartItem
from database.items import db_items
from kivymd.app import MDApp

from kivymd.uix.screen import MDScreen

Builder.load_file("itemscreen/ui.kv")


class ItemScreen(MDScreen):
    item = ObjectProperty(Item())
    incartitem = ObjectProperty(allownone=True)
    description = StringProperty("")
    price = NumericProperty(1)
    image = StringProperty("assets/images/item.jpg")
    stock = NumericProperty(1)
    amount = NumericProperty(1)
    background_color = ColorProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toolbar = None
        MDApp.get_running_app().bind(favorite=self.on_favorite_items)

    def add_to_favorite(self, _):
        from utils.image_colors import get_accent_color
        color = get_accent_color(self.ids.image._container.image)
        _.md_bg_color = color
        self.background_color = color

    def on_item(self, _, item):
        app = MDApp.get_running_app()

        self.ids.title.text = item.name
        self.description = item.description
        self.price = item.price
        self.image = item.image
        if self.image:
            color = get_accent_color(self.ids.image._container.image)
            self.background_color = color
        self.stock = item.stock
        self.incartitem = app.cart.get_widget(self.item.id)
        self.amount = self.incartitem.item_card.amount if self.incartitem else 0

        # simular display line
        self.ids.simular.params = {"category": self.item.category_id}

        # in favorite?
        heart_button = self.ids.heart_button
        if self.item.id in app.favorite:
            heart_button.icon = "heart"
            heart_button.icon_color = 1, 0, 0, 1
        else:
            heart_button.icon = "heart-outline"
            heart_button.icon_color = 0, 0, 0, 1

    def on_favorite_items(self, _, items):
        if not self.item:
            return
        button = self.ids.heart_button
        if self.item.id in items:
            button.icon = "heart"
            button.icon_color = 1, 0, 0, 1
        else:
            button.icon = "heart-outline"
            button.icon_color = 0, 0, 0, 1

    def favorite(self):
        app = MDApp.get_running_app()
        if app.username:
            self.item.favorite(app.set_favorite)
        else:
            app.request_login()

    def increase_item_amount(self):
        app = MDApp.get_running_app()
        db_items.add_items([self.item])
        if self.item.id not in app.cart.items:
            self.incartitem = app.cart.add_item(CartItem(item=self.item.data))
        else:
            if self.incartitem.item_card.amount < self.incartitem.c_item.item.stock:
                self.incartitem.item_card.amount += 1
            else:
                toast("we're out of stock")
        self.amount = self.incartitem.item_card.amount

    def decrease_item_amount(self):
        app = MDApp.get_running_app()
        db_items.add_items([self.item])
        if self.item.id in app.cart.items:
            if self.amount == 1:
                app.cart.remove_item(self.item.id)
                self.amount = 0
            else:
                self.incartitem.item_card.amount -= 1
                self.amount = self.incartitem.item_card.amount

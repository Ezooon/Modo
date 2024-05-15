from kivy.metrics import dp
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import NumericProperty, ListProperty

from database.messages import db_messages
from uix.incartitem import InCartSwipeItem
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.toast import toast
from kivymd.app import MDApp

from api.cart import Cart

Builder.load_file("home/cart/ui.kv")


class CartTap(MDBottomNavigationItem):
    total = NumericProperty(0)
    items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ordered_cart = None
        self.focused_item = None

    def add_item(self, c_item):
        if c_item.item.id in self.items:
            toast(f"{c_item.name} is already in cart")
        self.items.append(c_item.item.id)

        itemx = InCartSwipeItem(c_item=c_item)
        itemx.pressed = self.change_amount
        self.ids.items_list.add_widget(itemx)
        return itemx

    def remove_item(self, id):
        items_list = self.ids.items_list
        for itemx in items_list.children:
            if itemx.c_item.item.id == id:
                items_list.remove_widget(itemx)
                self.items.remove(id)
                break

    def get_widget(self, item_id):
        items = self.ids.items_list.children
        for itemx in items:
            if itemx.c_item.item.id == item_id:
                return itemx

    def increase_item_amount(self, id):
        items = self.ids.items_list.children
        for itemx in items:
            if itemx.c_item.id == id:
                stock = itemx.item.stock
                if itemx.item_card.amount < stock:
                    itemx.item_card.amount += 1
                else:
                    toast("we're out of stock")
                return itemx.item_card.amount

    def decrease_item_amount(self, id):
        items = self.ids.items_list.children
        for itemx in items:
            if itemx.c_item.id == id:
                if itemx.item_card.amount > 1:
                    itemx.item_card.amount -= 1
                return itemx.item_card.amount

    def change_amount(self, itemx):
        print("less shit")
        self.focused_item = itemx
        self.ids.amount_label.text = "X" + str(itemx.item_card.amount)
        Animation(y=dp(31), d=0.1).start(self.ids.total_box)

    def on_touch_down(self, touch):
        if not self.ids.amount_box.collide_point(*self.to_local(*touch.pos)):
            Animation(y=0, d=0.1).start(self.ids.total_box)
        return super().on_touch_down(touch)

    def order(self):
        c_items = [widget.c_item for widget in self.ids.items_list.children]
        self.ordered_cart = Cart(c_items=c_items)
        self.ordered_cart.order(self.ordered)

    def ordered(self, cart):
        app = MDApp.get_running_app()
        db_messages.add_messages([cart.message])
        app.chat_screen.add_messages([cart.message])
        self.parent.parent.parent.parent.current = "chat_screen"


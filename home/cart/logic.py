from kivy.metrics import dp
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import NumericProperty, ListProperty

from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from uix.incartitem import InCartItem
from kivymd.toast import toast

Builder.load_file("home/cart/ui.kv")


class CartTap(MDBottomNavigationItem):
    total = NumericProperty(0)
    items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.focused_item = None

    def add_item(self, item):
        if item.id in self.items:
            toast(f"{item.name} is already in cart")
        self.items.append(item.id)

        itemx = InCartItem(item=item, size_hint=(0.6, None), height=50)
        itemx.pressed = self.change_amount
        self.ids.items_list.add_widget(itemx)

    def remove_item(self, id):
        items_list = self.ids.items_list
        for itemx in items_list.children:
            if itemx.item.id == id:
                items_list.remove_widget(itemx)
                self.items.remove(id)
                break

    def increase_item_amount(self, id):
        items = self.ids.items_list.children
        for itemx in items:
            if itemx.item.id == id:
                stock = itemx.item.stock
                if itemx.amount < stock:
                    itemx.amount += 1
                else:
                    toast("we're out of stock")

    def decrease_item_amount(self, id):
        items = self.ids.items_list.children
        for itemx in items:
            if itemx.item.id == id:
                if itemx.amount > 1:
                    itemx.amount -= 1

    def change_amount(self, itemx):
        self.focused_item = itemx
        self.ids.amount_label.text = "X" + str(itemx.amount)
        Animation(y=dp(31), d=0.1).start(self.ids.total_box)

    def on_touch_down(self, touch):
        if not self.ids.amount_box.collide_point(*self.to_local(*touch.pos)):
            Animation(y=0, d=0.1).start(self.ids.total_box)
        return super().on_touch_down(touch)

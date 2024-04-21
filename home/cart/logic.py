from kivy.lang import Builder
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.properties import NumericProperty
Builder.load_file("home/cart/ui.kv")


class CartTap(MDBottomNavigationItem):
    total = NumericProperty(0)

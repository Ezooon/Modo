from kivy.uix.image import AsyncImage
from kivy.lang import Builder
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
Builder.load_file("home/shop/ui.kv")


class TopScrollView(MDScrollView):
    pass


class ShopTap(MDBottomNavigationItem):
    pass

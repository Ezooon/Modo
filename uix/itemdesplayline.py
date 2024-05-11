from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.spinner import MDSpinner
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.metrics import dp
from api.item import Item, db_items
from api.cart import CartItem
from kivy.loader import Loader
from kivymd.app import MDApp

Loader.loading_image = "assets/item.jpg"
Builder.load_string("""
<ItemCard>:
    size_hint: None, 1
    width: self.height
    source: root.image
    box_radius: [0, 0, 24, 24]
    box_color: self.theme_cls.opposite_bg_normal[:3] + [0.5]
    radius: dp(24)
    BoxLayout:
        orientation: "vertical"
        padding: 0
        spacing: dp(10)
        MDLabel:
            text: root.name
            halign: "right"
            pos_hint: {"center_y": 0.5}
            shorten_from: "left"
            shorten: True
            font_size: sp(14)
            color: self.theme_cls.bg_normal
            outline_color: self.theme_cls.opposite_bg_normal
            outline_width: sp(1)
        MDLabel:
            text: str(root.price) + " SDG"
            font_style: "Caption"
            font_size: sp(12)
            color: self.theme_cls.bg_normal
            outline_color: 0,0,0,1
            outline_width: sp(1)
            
    MDFloatLayout:
        size_hint: None, None
        size: 0, 0
        MDIconButton:
            id: heart_button
            icon: "heart-outline"
            pos: root.width - dp(48), root.height - dp(48)
            theme_text_color: "Custom"
            on_release:
                root.favorite(self)
                
        MDIconButton:
            id: cart_button
            icon: "cart-plus"
            theme_text_color: "Custom"
            pos: 0, root.height - dp(48)
            md_bg_color: 0, 0 , 0 ,0.001
            on_release:
                root.to_cart(self)

<ItemDisplayLine>:
    orientation: "vertical"
    size_hint: 1, None
    MDBoxLayout:
        size_hint: 1, None
        height: dp(40) 
        padding: dp(10)
        MDIconButton:
            id: button
            icon: "arrow-left"
            pos_hint: {"center_y": 0.5}
            on_release: root.button_release(self.icon)
        MDLabel:
            text: root.title
            halign: "right"
            font_style: "Subtitle1"
            
    RecycleView:
        id: recycle_view
        viewclass: "ItemCard"
        size_hint: 1, 1
        bar_inactive_color: 1,1,1,0
        bar_color: 1,1,1,0
        data: root.data
        do_scroll_y: False
        scroll_timeout: 500
        MDRecycleGridLayout:
            id: content
            orientation: "rl-tb"
            size_hint: None, 1
            rows: 1
            adaptive_width: True
            padding: dp(5)
            spacing: dp(10)

""")


class ItemCard(MDSmartTile):
    item = ObjectProperty(Item())
    name = StringProperty("")
    description = StringProperty("")
    price = NumericProperty(1)
    image = StringProperty("assets/item.jpg")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        MDApp.get_running_app().cart.bind(items=self.on_cart_items)
        MDApp.get_running_app().bind(favorite=self.on_favorite_items)

    def on_cart_items(self, _, items):
        button = self.ids.cart_button
        if self.item.id in items:
            button.icon = "cart"
            button.icon_color = "#ffd700"
        else:
            button.icon = "cart-plus"
            button.icon_color = "#000000"

    def on_favorite_items(self, _, items):
        button = self.ids.heart_button
        if self.item.id in items:
            button.icon = "heart"
            button.icon_color = 1, 0, 0, 1
        else:
            button.icon = "heart-outline"
            button.icon_color = 0, 0, 0, 1

    def on_item(self, _, item):
        app = MDApp.get_running_app()

        self.name = item.name
        self.description = item.description
        self.price = item.price
        self.image = item.image

        # in cart?
        cart_button = self.ids.cart_button
        if self.item.id in app.cart.items:
            cart_button.icon = "cart"
            cart_button.icon_color = "#ffd700"
        else:
            cart_button.icon = "cart-plus"
            cart_button.icon_color = "#000000"

        # in favorite?
        heart_button = self.ids.heart_button
        if self.item.id in app.favorite:
            heart_button.icon = "heart"
            heart_button.icon_color = 1, 0, 0, 1
        else:
            heart_button.icon = "heart-outline"
            heart_button.icon_color = 0, 0, 0, 1

    def on_release(self):
        sm = MDApp.get_running_app().root
        sm.get_screen("item_screen").item = self.item
        sm.current = "item_screen"

    def favorite(self, button):
        app = MDApp.get_running_app()
        self.item.favorite(app.set_favorite)

    def to_cart(self, button):
        app = MDApp.get_running_app()
        db_items.add_items([self.item])
        if self.item.id in app.cart.items:
            app.cart.remove_item(self.item.id)
        else:
            app.cart.add_item(CartItem(item=self.item.data))


class ItemDisplayLine(MDBoxLayout):
    title = StringProperty("")
    data = ListProperty([])

    def __init__(self, **kwargs):
        super(ItemDisplayLine, self).__init__(**kwargs)
        Clock.schedule_once(self.start, 1)
        self.spinner = MDSpinner(size=(dp(40), dp(40)))
        floating = FloatLayout(size=(0, 0))
        self.add_widget(floating)
        floating.size_hint = (None, None)
        floating.add_widget(self.spinner)

    def start(self, _):
        self.spinner.size_hint = (None, None)
        self.spinner.y = self.center_y - dp(20)
        self.spinner.x = self.center_x
        self.load()

    def load(self):
        self.ids.recycle_view.data = []
        Item.get_items(self._load_items, on_failure=self.fail_to_load)
        self.spinner.active = True

    def _load_items(self, items):
        """populating the desplay line with item widgets"""
        data = self.ids.recycle_view.data + [{"item": item, "size_hint": (None, 1)} for item in items]
        self.ids.recycle_view.data = data
        self.ids.recycle_view.scroll_x = 1
        self.spinner.active = False
        self.ids.button.icon = "arrow-left"

    def fail_to_load(self, *args):
        """called on a network error or a request failure"""
        self.ids.button.icon = "reload"
        self.spinner.active = False

    def button_release(self, icon):
        """called when the more or reload button press"""
        if icon == "reload":
            self.load()
            return
        # ToDO when it's left-arrow

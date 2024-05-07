from kivymd.uix.card import MDCardSwipe
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.lang import Builder

Builder.load_string("""
<InCartItem>:
    height: dp(50)
    md_bg_color: 1,1,1,0
    on_swipe_complete:
        self.parent.remove_widget(self)
    MDCardSwipeLayerBox:
        md_bg_color: 1,0,0,1
    MDCardSwipeFrontBox:
        md_bg_color: 1,1,1,1
        radius: 0
        on_release: root.pressed(root)
        MDBoxLayout:
            orientation: "vertical"
            padding:  dp(5), dp(10), dp(5), 0
            MDLabel:
                text: root.name
                halign: "right"
            BoxLayout:
                MDLabel:
                    text: str(root.price * root.amount) + " SDG"
                    font_style: "Caption"
                MDLabel:
                    text: str(root.price) + " X " + str(root.amount) 
                    font_style: "Caption"
                    halign: "right"
        AsyncImage:
            size_hint: None, 1
            source: root.image
            width: self.height
            keep_ratio: False
""")


class InCartItem(MDCardSwipe):
    item = ObjectProperty()
    name = StringProperty("Item")
    image = StringProperty("assets/item.jpg")
    price = NumericProperty(100)
    amount = NumericProperty(1)

    def on_item(self, _, item):
        self.name = item.name
        self.image = item.image
        self.price = item.price

    def pressed(self, instance):
        pass

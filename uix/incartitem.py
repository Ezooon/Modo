from kivymd.uix.card import MDCardSwipe
from kivy.properties import NumericProperty, StringProperty
from kivy.lang import Builder

Builder.load_string("""
<InCartItem>:
    # size_hint: 1, None
    height: dp(50)
    md_bg_color: 1,1,1,0
    on_swipe_complete:
        self.parent.remove_widget(self)
    MDCardSwipeLayerBox:
    MDCardSwipeFrontBox:
        md_bg_color: 1,1,1,0.3
        radius: 0
        MDBoxLayout:
            orientation: "vertical"
            padding: dp(10)
            MDLabel:
                text: "A ringy paq"
                halign: "right"
            MDLabel:
                text: str(root.price) + " SDG"
                font_style: "Caption"
        Image:
            size_hint: None, 1
            source: "item.jpg"
            width: self.height
            keep_ratio: False
""")


class InCartItem(MDCardSwipe):
    price = NumericProperty(10000)

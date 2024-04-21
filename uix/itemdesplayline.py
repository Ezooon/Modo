from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.imagelist import MDSmartTile
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
Builder.load_string("""
<ItemCard>:
    size_hint: None, 1
    width: self.height
    source: "item.jpg"
    box_radius: [0, 0, 24, 24]
    box_color: 1, 1, 1, 0.5
    radius: dp(24)
    BoxLayout:
        orientation: "vertical"
        MDLabel:
            text: root.text
            halign: "right"
            pos_hint: {"center_y": 0.5}
            shorten_from: "left"
            shorten: True
        MDLabel:
            text: root.price
            font_style: "Caption"
            
    MDFloatLayout:
        size_hint: None, None
        size: 0, 0
        MDIconButton:
            icon: "heart-outline"
            pos: root.height - dp(48), root.height - dp(48)
            theme_text_color: "Custom"
            on_release:
                self.icon = "heart"
                self.icon_color = 1, 0 , 0 , 1
                
        MDIconButton:
            icon: "cart-plus"
            theme_text_color: "Custom"
            pos: 0, root.height - dp(48)
            md_bg_color: 0, 0 , 0 ,0.001
            on_release:
                self.icon = "cart"
                self.icon_color = rgba("#ffd700")
                self.md_bg_color = 1, 1, 1, 0.5


<ItemDisplayLine>:
    orientation: "vertical"
    size_hint: 1, None
    MDBoxLayout:
        size_hint: 1, None
        height: dp(40) 
        padding: dp(10)
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_y": 0.5}
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
        scroll_x: 1
        MDRecycleGridLayout:
            orientation: "rl-tb"
            size_hint: None, 1
            rows: 1
            adaptive_width: True
            padding: dp(5)
            spacing: dp(10)

""")


class ItemCard(MDSmartTile):
    text = StringProperty("")
    price = StringProperty("10000 SDG")


class ItemDisplayLine(MDBoxLayout):
    title = StringProperty("")
    data = ListProperty([])

    def __init__(self, **kwargs):
        super(ItemDisplayLine, self).__init__(**kwargs)
        Clock.schedule_once(self.start_right, 1)

    def start_right(self, _):
        self.ids.recycle_view.bind(children=self.rv_add_widget)

    def rv_add_widget(self):
        self.ids.recycle_view.scroll_x = 1

from kivy.metrics import dp
from kivymd.app import MDApp

from api.message import Message, db_messages
from uix.chatbubbles import ChatBubble, ReceivedBubble, CartBubble
from kivymd.uix.screen import MDScreen
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_file("chatscreen/ui.kv")


class ChatScreen(MDScreen):
    data = ListProperty([])

    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        messages_data = db_messages.get_all()
        messages = []
        for data in messages_data:
            messages.append(Message(**data))
        Clock.schedule_once(lambda x: self.add_messages(messages), 0)

    def on_enter(self, *args):
        if self.ids:
            self.ids.sv.scroll_y = 0
        self.ids.sv.refresh_from_data()

    def send(self, text_field):
        text = text_field.text
        msg = Message(content=text)
        MDApp.get_running_app().send_list.append(msg)
        if text.startswith('C{"id": '):
            self.data.append({"viewclass": 'CartBubble', "message": msg,
                              "size_hint": (1, None)})
        else:
            self.data.append({"viewclass": 'ChatBubble', "message": msg,
                              "size_hint": (1, None)})
        text_field.text = ""
        self.ids.sv.refresh_from_data()

    def add_messages(self, messages):
        data = []
        for msg in messages:
            if msg.id not in ChatBubble.BUBBLES:
                if msg.content.startswith('C{"id": '):
                    data.append({"viewclass": 'CartBubble', "message": msg,
                                 "size_hint": (1, None)})
                elif msg.sent_to_user:
                    data.append({"viewclass": 'ReceivedBubble', "message": msg,
                                 "size_hint": (1, None)})
                else:
                    data.append({"viewclass": 'ChatBubble', "message": msg,
                                 "size_hint": (1, None)})
            if not msg.sent:
                MDApp.get_running_app().send_list.append(msg)

        if data:
            self.data = self.data + data
            self.ids.sv.scroll_y = 0
            self.ids.sv.refresh_from_data()

from api.message import Message, db_messages
from uix.chatbubbles import ChatBubble, ReceivedBubble, CartBubble
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_file("chatscreen/ui.kv")


class ChatScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        messages_data = db_messages.get_all()
        messages = []
        for data in messages_data:
            messages.append(Message(**data))
        Clock.schedule_once(lambda x: self.add_messages(messages), 0)

    def send(self, text):
        bubble = ChatBubble(message=Message(content=text))
        self.ids.messages.add_widget(bubble)

    def add_messages(self, messages):
        for msg in messages:
            if msg.id not in ChatBubble.BUBBLES:
                if msg.sent_by_user:
                    self.ids.messages.add_widget(ChatBubble(message=msg))
                else:
                    self.ids.messages.add_widget(ReceivedBubble(message=msg))

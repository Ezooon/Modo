from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.lang import Builder
from kivy.clock import Clock

from datetime import datetime
from api.message import Message

Builder.load_file("uix/chatbubbles.kv")


def am_pm(t):
    hh = t.hour if t.hour <= 12 else t.hour - 12
    c = "am" if t.hour <= 12 else "pm"
    mm = t.minute if t.minute > 9 else "0" + str(t.minute)
    return f"{hh}:{mm} {c}"


class BubbleBase(MDBoxLayout):
    BUBBLES = {}
    message = ObjectProperty()

    text = StringProperty("...")
    sent = StringProperty("12:00 pm")
    status = NumericProperty(0)
    #  0: not sent
    #  1: sent
    #  2: delivered
    #  3: read

    def __init__(self, **kwargs):
        super(BubbleBase, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_message, 5)

    def update_message(self, _):
        if self.message:
            self.message = Message.MESSAGES[self.message.id]
            return not self.message.delivered  # ToDo make it not self.message.read when you implement the read function

    def on_message(self, _, msg):
        BubbleBase.BUBBLES[msg.id] = self
        self.text = msg.content
        self.status = bool(msg.sent) + msg.delivered + msg.read
        sent = msg.sent or datetime.now()
        self.sent = am_pm(sent.time())


class ChatBubble(BubbleBase):

    def on_message(self, _, message):
        super(ChatBubble, self).on_message(_, message)

        def on_failure(_):
            Clock.schedule_once(lambda x: self.message.send(), 5)

        if not message.sent:
            message.send(on_failure=on_failure)


class CartBubble(BubbleBase):
    pass


class ReceivedBubble(BubbleBase):
    pass


from .apirequest import api_request, MDApp
from datetime import datetime
from database.messages import db_messages


class Message:
    MESSAGES = {}
    unread = {}
    db_messages = db_messages

    def __init__(self, **data):
        self.data = data

        # setting attributes
        self._on_data(data)

        # add to All MESSAGES
        Message.MESSAGES[self.id] = self

    def _on_data(self, data):
        auto_id = min(Message.MESSAGES.keys() or [1])
        auto_id = 0 if auto_id > 1 else auto_id - 1

        self.id = data.get("id") or auto_id
        self.sent_by = data.get("sent_by") or -1
        self.sent_to = data.get("sent_to") or -1
        self.content = data.get("content") or "..."
        self.delivered = data.get("delivered") or False
        self.read = data.get("read") or False
        self.sent = None
        if data.get("sent"):
            self.sent = datetime.fromisoformat(data.get("sent"))

        self.sent_by_user = self.sent_by == MDApp.get_running_app().user.id
        self.sent_to_user = self.sent_to == MDApp.get_running_app().user.id

        if self.sent and self.sent_by_user:
            if not self.delivered:  # ToDo this should be read
                Message.unread[self.id] = self
            elif self.id in Message.unread.keys():
                Message.unread[self.id] = self

    def send(self, on_success=lambda _: None, on_failure=lambda *_: None, **kwargs):

        def sent(_, data):
            db_messages.replace(self.id, data)
            Message.MESSAGES.pop(self.id)

            self._on_data(data)

            Message.MESSAGES[self.id] = self

            on_success(self)

        def failure(*args):
            return on_failure(self, *args)

        body = {
            "sent_by": MDApp.get_running_app().user.id,
            "content": self.content,
        }

        api_request("chat/messages/", sent, method="POST", body=body, on_failure=failure, **kwargs)

    @classmethod
    def refresh_unread(cls, on_success=lambda x: None, **kwargs):
        """update the stats of the un read messages"""
        def message_wrapper(thread, response):
            messages_data = response
            messages = []
            for data in messages_data:
                msg = cls.MESSAGES[data["id"]]
                msg._on_data(data)
                if msg.id in Message.unread.keys() and msg.delivered:  # ToDo this should be read
                    Message.unread.pop(msg.id)
                messages.append(msg)

            db_messages.add_messages(messages)
            on_success(messages)

        if cls.unread:
            api_request("chat/messages/", message_wrapper, body={"wait_list": list(cls.unread.keys())}, **kwargs)

    @classmethod
    def get_undelivered_messages(cls, on_success=lambda x: None, **kwargs):
        def message_wrapper(thread, response):
            messages_data = response
            messages = []
            for data in messages_data:
                messages.append(Message(**data))
            db_messages.add_messages(messages)
            if messages:
                cls.mark_delivered()
            on_success(messages)

        api_request("chat/messages/", message_wrapper,
                    params={"delivered": False, "sent_to": MDApp.get_running_app().user.id}, **kwargs)

    @classmethod
    def get_all_messages(cls, on_success=lambda x: None, **kwargs):
        def message_wrapper(thread, response):
            messages_data = response
            messages = []
            for data in messages_data:
                messages.append(Message(**data))
            db_messages.add_messages(messages)
            if messages:
                cls.mark_delivered()
            on_success(messages)

        i = MDApp.get_running_app().user.chat
        api_request("chat/messages/", message_wrapper,
                    params={"chat": i}, **kwargs)

    @classmethod
    def mark_delivered(cls):
        """sends a request to mark all the undelivered messages to the user's chat as delivered"""
        api_request("chat/messages/", print, method="PUT",
                    params={"delivered": False, "sent_to": MDApp.get_running_app().user.id})

    @classmethod
    def get_not_sent(cls):
        msgs_data = cls.db_messages.get_all(sent=None)
        send_list = [Message(**data) for data in msgs_data]
        return send_list

    def __repr__(self):
        short_content = str(self.content)
        if self.sent_by_user:
            chatting_with = "to: " + str(self.sent_to)
        else:
            chatting_with = "from: " + str(self.sent_by)
        if len(short_content) > 30:
            short_content = short_content[:30] + "..."

        return f"<{self.id} {chatting_with}: \"{short_content}\">"


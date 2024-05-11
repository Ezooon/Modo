from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.toast import toast
from kivy.properties import StringProperty, ObjectProperty, ListProperty, BooleanProperty
from kivy.clock import Clock


class SM(ScreenManager):
    pass


class ModoApp(MDApp):
    online = BooleanProperty()

    user = ObjectProperty()
    username = StringProperty("")
    email = StringProperty("")

    cart = ObjectProperty()

    favorite = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None
        self.user_api_token = None
        self.chat_screen = None

    def build_config(self, config):
        config.setdefaults("App", {
            "saved cart": [],
            "first launch": True,
        })

        config.setdefaults("Account", {
            "id": 0,
            "username": "",
            "email": "",
            "user_api_token": "",
        })

    def build(self):
        # account
        from api.account import Account

        self.user_id = self.config.getint("Account", "id")
        self.username = self.config.get("Account", "username")
        self.email = self.config.get("Account", "email")
        self.user_api_token = self.config.get("Account", "user_api_token")

        self.user = Account(id=self.user_id, username=self.username, email=self.email).full_data()

        # favorites
        self.user.get_favorite(self.set_favorite, results="simple")

        sm = SM()
        self.theme_cls.primary_palette = "Amber"

        # load saved cart
        self.cart = sm.get_screen("home").ids.cart
        # conf_cart = self.config.get("App", "saved cart")  ToDo in another update
        # if conf_cart:
        #     cart_items = map(int, conf_cart.split(", "))
        #     self.cart.items = cart_items
        # else:
        #     self.cart.items = []

        # start chat check loop
        self.chat_screen = sm.get_screen("chat_screen")
        Clock.schedule_interval(self.check_new_messages, 5)

        # if the first launch start with the signup screen
        first_launch = self.config.getboolean("App", "first launch")  # ToDo uncomment this
        if first_launch:
            sm.current = "signup"
        else:
            sm.current = "home"
        self.config.set("App", "first launch", False)
        self.config.write()

        return sm

    def check_new_messages(self, dt):
        from api.message import Message

        def set_offline(*args):
            if self.online:
                self.online = False
                toast("You Are Offline", (1, 0, 0, 1))

        def set_online(*args):
            if not self.online:
                self.online = True
                toast("You Are Back Online", (0, 1, 0, 1))
            self.chat_screen.add_messages(*args)

        Message.get_undelivered_messages(set_online, on_failure=set_offline)
        Message.refresh_unread()

    def on_username(self, _, value):
        self.config.set("Account", "username", value)
        self.config.write()

    def on_email(self, _, value):
        self.config.set("Account", "email", value)
        self.config.write()

    def on_user_api_token(self, _, value):
        self.config.set("Account", "user_api_token", value)
        self.config.write()

    def set_favorite(self, results):
        self.favorite = [fitem['item'] for fitem in results]

    def on_stop(self):
        self.config.set("App", "saved cart", str(self.cart.items)[1:-1])
        self.config.write()


ModoApp().run()

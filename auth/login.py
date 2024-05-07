from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from api.account import Account
from kivymd.toast import toast
from kivymd.app import MDApp

Builder.load_file("auth/login.kv")


class Login(MDScreen):
    def login(self, username, password):
        Account.login(username, password, self.logged_in)

    def logged_in(self, data):
        app = MDApp.get_running_app()
        app.id = data["id"]
        app.username = data["username"]
        app.email = data["email"]
        app.user_api_token = data["token"]

        toast("Wellcome back " + data["username"])

        self.parent.current = "home"

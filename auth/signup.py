from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivymd.toast import toast
from kivymd.app import MDApp

Builder.load_file("auth/signup.kv")


class SignUp(MDScreen):
    def animate(self, p):
        """slide the sign-up information boxes"""
        if not (self.ids.username.text and self.ids.email.text):
            toast("Those fields are required")
            return

        box = self.ids.name_box

        Animation(x=-self.width*p, d=0.2).start(box)
        self.ids.password.focus = True

    def sign_up(self, username, email, password, password2):
        from api.account import Account
        if password != password2:
            toast("Passwords must match")
            return
        if len(password) < 6:
            toast("Passwords should contain at least 6 characters")
            return
        Account.sign_up(username, email, password, self.signed_up)

    def signed_up(self, data):
        app = MDApp.get_running_app()
        app.username = data["username"]
        app.email = data["email"]
        app.user_api_token = data["token"]

        toast("Wellcome " + data["username"])

        self.parent.current = "home"


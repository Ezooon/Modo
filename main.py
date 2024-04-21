from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager


class SM(MDScreenManager):
    pass


class ModoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Amber"
        # self.theme_cls.theme_style = "Dark"
        return SM()


ModoApp().run()

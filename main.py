"""
main.py — app entry point.

Loads the Add Payment and Summary tabs, with a simple tab bar at the
bottom to switch between them. The Expenses tab will be added the same
way in the next step.

Run with:  python main.py   (or, on this machine: py -3.12 main.py)
"""

import os
from kivy.utils import platform
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from db import MeetupDB
from screens.add_payment import AddPaymentScreen
from screens.summary import SummaryScreen
from screens.expenses import ExpensesScreen

Builder.load_file(os.path.join("kv", "addpayment.kv"))
Builder.load_file(os.path.join("kv", "summary.kv"))
Builder.load_file(os.path.join("kv", "expenses.kv"))
Builder.load_file(os.path.join("kv", "root.kv"))


class RootWidget(MDBoxLayout):
    def switch_tab(self, screen_name):
        self.ids.screen_manager.current = screen_name


class MeetupTrackerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"

        db_path = self._get_db_path()
        self.receipts_dir = self._get_receipts_dir()
        os.makedirs(self.receipts_dir, exist_ok=True)

        self.db = MeetupDB(db_path)

        root = RootWidget()
        sm = root.ids.screen_manager
        sm.add_widget(AddPaymentScreen(name="add_payment"))
        sm.add_widget(SummaryScreen(name="summary"))
        sm.add_widget(ExpensesScreen(name="expenses"))
        return root

    def _get_db_path(self):
        if platform == "android":
            return os.path.join(self.user_data_dir, "meetup.db")
        return os.path.join(os.getcwd(), "data", "meetup.db")

    def _get_receipts_dir(self):
        if platform == "android":
            return os.path.join(self.user_data_dir, "receipts")
        return os.path.join(os.getcwd(), "data", "receipts")


if __name__ == "__main__":
    MeetupTrackerApp().run()

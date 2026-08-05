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
    # Maps each screen name to the tab button that represents it, so we
    # can highlight whichever one is currently active.
    _TAB_BUTTON_IDS = {
        "add_payment": "btn_add_payment",
        "summary": "btn_summary",
        "expenses": "btn_expenses",
    }

    def switch_tab(self, screen_name):
        self.ids.screen_manager.current = screen_name
        self.update_active_tab(screen_name)

    def update_active_tab(self, active_screen_name):
        app = MDApp.get_running_app()
        active_color = app.theme_cls.primary_color
        inactive_color = (0.5, 0.5, 0.5, 1)  # muted grey
        for screen_name, button_id in self._TAB_BUTTON_IDS.items():
            button = self.ids[button_id]
            is_active = screen_name == active_screen_name
            # KivyMD buttons ignore text_color unless theme_text_color is
            # set to "Custom" first - otherwise they keep following the
            # app's theme and our color change has no visible effect.
            button.theme_text_color = "Custom"
            button.text_color = active_color if is_active else inactive_color
            # MDFlatButton has no real "bold" property, so we use a
            # slightly larger font for the active tab as the highlight
            # instead - guaranteed to render, unlike a fake attribute.
            button.font_size = "15sp" if is_active else "13sp"


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
        root.update_active_tab("add_payment")
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

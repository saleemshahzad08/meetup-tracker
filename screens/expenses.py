"""
screens/expenses.py — Tab 3: Expenses.

Lets the user log what was bought for the meetup (item/service + amount),
see a running total spent, and browse past expenses. Tapping an expense
opens a small menu to edit or delete it.
"""

from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField


class ExpensesScreen(Screen):
    def on_pre_enter(self, *args):
        self.refresh_list()
        self.update_total()

    def save_expense(self):
        item = self.ids.item_field.text.strip()
        amount_text = self.ids.amount_field.text.strip()

        if not item:
            self._show_message("Please enter what the money was spent on.")
            return
        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            self._show_message("Please enter a valid amount greater than 0.")
            return

        app = MDApp.get_running_app()
        app.db.add_expense(item, amount)

        # Reset the form for the next entry
        self.ids.item_field.text = ""
        self.ids.amount_field.text = ""

        self.refresh_list()
        self.update_total()

    def update_total(self):
        app = MDApp.get_running_app()
        total = app.db.total_spent()
        self.ids.total_label.text = f"Total spent: {total:.2f}"

    def refresh_list(self):
        app = MDApp.get_running_app()
        self.ids.expenses_list.clear_widgets()
        for expense in app.db.list_expenses():
            item_widget = OneLineListItem(
                text=f"{expense['item']} — {expense['amount']:.2f}"
            )
            item_widget.bind(
                on_release=lambda inst, e=expense: self.open_expense_menu(e)
            )
            self.ids.expenses_list.add_widget(item_widget)

    # ---------- Tap-to-open menu: edit / delete ----------

    def open_expense_menu(self, expense):
        self._dialog = MDDialog(
            title=f"{expense['item']} — {expense['amount']:.2f}",
            text=f"Date: {expense['timestamp']}",
            buttons=[
                MDFlatButton(text="Edit", on_release=lambda x: self._edit_expense(expense)),
                MDFlatButton(text="Delete", on_release=lambda x: self._confirm_delete(expense)),
                MDFlatButton(text="Close", on_release=lambda x: self._dialog.dismiss()),
            ],
        )
        self._dialog.open()

    def _edit_expense(self, expense):
        self._dialog.dismiss()

        form = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="120dp")
        item_field = MDTextField(text=expense["item"], hint_text="What was it for?")
        amount_field = MDTextField(
            text=str(expense["amount"]), hint_text="Amount", input_filter="float"
        )
        form.add_widget(item_field)
        form.add_widget(amount_field)

        def do_save(*args):
            new_item = item_field.text.strip()
            try:
                new_amount = float(amount_field.text.strip())
                if new_amount <= 0:
                    raise ValueError
            except ValueError:
                self._show_message("Please enter a valid amount greater than 0.")
                return
            if not new_item:
                self._show_message("Please enter what the money was spent on.")
                return
            app = MDApp.get_running_app()
            app.db.update_expense(expense["id"], item=new_item, amount=new_amount)
            edit_dialog.dismiss()
            self.refresh_list()
            self.update_total()

        edit_dialog = MDDialog(
            title="Edit Expense",
            type="custom",
            content_cls=form,
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: edit_dialog.dismiss()),
                MDRaisedButton(text="Save", on_release=do_save),
            ],
        )
        edit_dialog.open()

    def _confirm_delete(self, expense):
        self._dialog.dismiss()

        def do_delete(*args):
            app = MDApp.get_running_app()
            app.db.delete_expense(expense["id"])
            confirm_dialog.dismiss()
            self.refresh_list()
            self.update_total()

        confirm_dialog = MDDialog(
            title="Delete this expense?",
            text=f"{expense['item']} — {expense['amount']:.2f}\nThis can't be undone.",
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: confirm_dialog.dismiss()),
                MDRaisedButton(text="Delete", on_release=do_delete),
            ],
        )
        confirm_dialog.open()

    def _show_message(self, text):
        dialog = MDDialog(
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

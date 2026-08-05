"""
screens/summary.py — Tab 2: Summary.

Shows total collected, total spent, and the remaining balance — all
calculated fresh from the database every time this tab is opened. Also
hosts:
  - "Export Data": zips the database + every receipt into a backup file.
  - "Start Fresh": wipes all payments/expenses/receipts so the app can
    be reused for a new meetup. Requires a confirmation, since it's
    irreversible.
"""

from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton

from utils.export import export_data, get_export_dir
from utils.reset import clear_receipts
from utils.report_export import generate_markdown_report, get_report_filename


class SummaryScreen(Screen):
    def on_pre_enter(self, *args):
        self.refresh()

    def refresh(self):
        app = MDApp.get_running_app()
        collected = app.db.total_collected()
        spent = app.db.total_spent()
        balance = collected - spent

        self.ids.collected_label.text = f"Total collected: {collected:.2f}"
        self.ids.spent_label.text = f"Total spent: {spent:.2f}"
        self.ids.balance_label.text = f"Remaining balance: {balance:.2f}"

    # ---------- Export ----------

    def export_data(self):
        app = MDApp.get_running_app()
        try:
            export_dir = get_export_dir()
            zip_path = export_data(app.db.db_path, app.receipts_dir, export_dir)
        except Exception as e:
            self._show_message(f"Export failed: {e}")
            return

        self._show_message(
            "Backup created:\n\n"
            f"{zip_path}\n\n"
            "Copy this file somewhere safe (e.g. your PC, Google Drive app, "
            "or email it to yourself) to keep it backed up."
        )

    # ---------- Markdown Report ----------

    def export_report(self):
        app = MDApp.get_running_app()
        try:
            payments = app.db.list_payments()
            expenses = app.db.list_expenses()
            totals = {
                "collected": app.db.total_collected(),
                "spent": app.db.total_spent(),
                "balance": app.db.balance(),
            }
            report_dir = get_export_dir()
            output_path = f"{report_dir}/{get_report_filename()}"
            report_path = generate_markdown_report(payments, expenses, totals, output_path)
        except Exception as e:
            self._show_message(f"Report export failed: {e}")
            return

        self._show_message(
            "Report created:\n\n"
            f"{report_path}\n\n"
            "This report lists payments, expenses, and totals only - no "
            "receipt photos are included. Open it with any text app, or "
            "a Markdown viewer for nicer formatting."
        )

    # ---------- Start Fresh ----------

    def confirm_start_fresh(self):
        self._confirm_dialog = MDDialog(
            title="Start a fresh meetup?",
            text=(
                "This will permanently delete ALL payments, expenses, "
                "and receipt images currently in the app.\n\n"
                "Have you exported a backup of this meetup's data first? "
                "This cannot be undone."
            ),
            buttons=[
                MDFlatButton(
                    text="Cancel", on_release=lambda x: self._confirm_dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Start Fresh", on_release=lambda x: self._do_start_fresh()
                ),
            ],
        )
        self._confirm_dialog.open()

    def _do_start_fresh(self):
        self._confirm_dialog.dismiss()
        app = MDApp.get_running_app()
        try:
            app.db.reset_all()
            clear_receipts(app.receipts_dir)
        except Exception as e:
            self._show_message(f"Couldn't start fresh: {e}")
            return
        self.refresh()
        self._show_message("All data cleared. Ready for a new meetup.")

    # ---------- Helper ----------

    def _show_message(self, text):
        dialog = MDDialog(
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

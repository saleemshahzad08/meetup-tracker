"""
screens/add_payment.py — Tab 1: Add Payment.

Lets the user enter a name + amount, optionally attach a receipt image
from the gallery, save it, see the running total, and browse past
payments. Tapping a payment opens a small menu to view its receipt,
edit the name/amount, or delete the entry.

Note on "Take Photo": plyer's direct camera capture has a long-standing,
unresolved bug on modern Android (a FileUriExposedException) that
requires deep native manifest changes to fix properly. Rather than ship
a button that reliably fails, we guide the user to use their phone's
own camera app and then attach the photo via "Pick from Gallery" -
which achieves the same result.

Note on "Pick from Gallery": plyer's Android gallery picker turned out
to be unreliable too - it tries to resolve a "real" file path internally
and increasingly fails to do so on modern Android, silently passing
None through instead of the picked file. So on Android, this screen
bypasses plyer entirely and talks to Android's own document picker
directly (the same lower-level system plyer itself wraps), which avoids
that buggy resolution step. Desktop testing still uses plyer, since
that path works fine there.
"""

import os
import shutil
import uuid

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

try:
    from plyer import filechooser
except Exception:
    filechooser = None

_GALLERY_REQUEST_CODE = 51341  # arbitrary but fixed, just needs to be unique


class AddPaymentScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pending_receipt_path = None
        if platform == "android":
            # Bind exactly once (here, not inside pick_from_gallery) so
            # repeated taps don't stack up duplicate result handlers.
            from android import activity  # noqa: p4a-provided, Android only

            activity.bind(on_activity_result=self._on_android_activity_result)

    def on_pre_enter(self, *args):
        self._pending_receipt_path = None
        self.refresh_list()
        self.update_total()

    # ---------- Receipt attach ----------

    def pick_from_gallery(self):
        if platform == "android":
            self._pick_from_gallery_android()
        else:
            self._pick_from_gallery_desktop()

    def _pick_from_gallery_desktop(self):
        if filechooser is None:
            self._show_message("Gallery picker isn't available on this system.")
            return
        try:
            filechooser.open_file(
                on_selection=self._on_desktop_file_selected,
                filters=[("Images", "*.jpg", "*.jpeg", "*.png")],
            )
        except Exception as e:
            self._show_message(f"Couldn't open gallery: {e}")

    def _pick_from_gallery_android(self):
        try:
            from android import mActivity
            from jnius import autoclass

            Intent = autoclass("android.content.Intent")
            intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
            intent.addCategory(Intent.CATEGORY_OPENABLE)
            intent.setType("image/*")
            mActivity.startActivityForResult(intent, _GALLERY_REQUEST_CODE)
        except Exception as e:
            self._show_message(f"Couldn't open gallery: {e}")

    def _on_android_activity_result(self, request_code, result_code, intent):
        if request_code != _GALLERY_REQUEST_CODE:
            return
        if result_code != -1:  # Android's Activity.RESULT_OK == -1
            return  # user backed out of the picker - nothing to do
        if intent is None:
            return
        uri = intent.getData()
        if uri is None:
            return
        # This callback fires from Android's own activity-result thread,
        # not Kivy's main thread - hand off to the main thread before
        # touching any widgets, same reasoning as the desktop path below.
        Clock.schedule_once(lambda dt: self._handle_android_uri(uri), 0)

    def _handle_android_uri(self, uri):
        app = MDApp.get_running_app()
        dest_name = f"{uuid.uuid4().hex}.jpg"
        dest_path = os.path.join(app.receipts_dir, dest_name)
        try:
            self._copy_content_uri(uri, dest_path)
        except Exception as e:
            self._show_message(f"Couldn't save receipt image: {e}")
            return
        self._pending_receipt_path = dest_path
        self.ids.receipt_status_label.text = f"Receipt attached: {dest_name}"

    def _copy_content_uri(self, uri, dest_path):
        """Reads the bytes behind an Android content:// Uri object and
        writes them to a normal file, via Android's own ContentResolver
        (the only reliable way to read a picked gallery image)."""
        from jnius import autoclass

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        activity_obj = PythonActivity.mActivity
        resolver = activity_obj.getContentResolver()
        input_stream = resolver.openInputStream(uri)
        try:
            chunk = bytearray(8192)
            with open(dest_path, "wb") as out_file:
                while True:
                    n = input_stream.read(chunk)
                    if n == -1:
                        break
                    out_file.write(bytes(chunk[:n]))
        finally:
            input_stream.close()

    def take_photo(self):
        self._show_message(
            "Direct camera capture isn't supported yet.\n\n"
            "Instead: take the photo with your phone's regular camera "
            "app, then come back here and tap \"Pick from Gallery\" to "
            "attach it."
        )

    # ---------- Desktop-only file handling (plyer path) ----------

    def _on_desktop_file_selected(self, selection):
        Clock.schedule_once(lambda dt: self._handle_desktop_selection(selection), 0)

    def _handle_desktop_selection(self, selection):
        if not selection or not selection[0]:
            return
        source_path = selection[0]
        app = MDApp.get_running_app()
        dest_name = f"{uuid.uuid4().hex}.jpg"
        dest_path = os.path.join(app.receipts_dir, dest_name)
        try:
            shutil.copy(source_path, dest_path)
        except Exception as e:
            self._show_message(f"Couldn't save receipt image: {e}")
            return
        self._pending_receipt_path = dest_path
        self.ids.receipt_status_label.text = f"Receipt attached: {dest_name}"

    # ---------- Save ----------

    def save_payment(self):
        name = self.ids.name_field.text.strip()
        amount_text = self.ids.amount_field.text.strip()

        if not name:
            self._show_message("Please enter a name.")
            return
        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            self._show_message("Please enter a valid amount greater than 0.")
            return

        app = MDApp.get_running_app()
        app.db.add_payment(name, amount, receipt_path=self._pending_receipt_path)

        # Reset the form for the next entry
        self.ids.name_field.text = ""
        self.ids.amount_field.text = ""
        self.ids.receipt_status_label.text = "No receipt attached"
        self._pending_receipt_path = None

        self.refresh_list()
        self.update_total()

    # ---------- List + running total ----------

    def update_total(self):
        app = MDApp.get_running_app()
        total = app.db.total_collected()
        self.ids.total_label.text = f"Total collected: {total:.2f}"

    def refresh_list(self):
        app = MDApp.get_running_app()
        self.ids.payments_list.clear_widgets()
        for payment in app.db.list_payments():
            item = OneLineAvatarIconListItem(
                text=f"{payment['name']} — {payment['amount']:.2f}"
            )
            item.bind(on_release=lambda inst, p=payment: self.open_payment_menu(p))
            self.ids.payments_list.add_widget(item)

    # ---------- Tap-to-open menu: view / edit / delete ----------

    def open_payment_menu(self, payment):
        has_receipt = bool(payment.get("receipt_path")) and os.path.exists(
            payment.get("receipt_path", "")
        )
        buttons = []
        if has_receipt:
            buttons.append(
                MDFlatButton(text="View Receipt", on_release=lambda x: self._view_receipt(payment))
            )
        buttons += [
            MDFlatButton(text="Edit", on_release=lambda x: self._edit_payment(payment)),
            MDFlatButton(text="Delete", on_release=lambda x: self._confirm_delete(payment)),
            MDFlatButton(text="Close", on_release=lambda x: self._dialog.dismiss()),
        ]
        self._dialog = MDDialog(
            title=f"{payment['name']} — {payment['amount']:.2f}",
            text=f"Date: {payment['timestamp']}",
            buttons=buttons,
        )
        self._dialog.open()

    def _view_receipt(self, payment):
        self._dialog.dismiss()
        content = Image(source=payment["receipt_path"])
        popup = Popup(
            title=f"{payment['name']} — {payment['amount']:.2f}",
            content=content,
            size_hint=(0.9, 0.9),
        )
        popup.open()

    def _edit_payment(self, payment):
        self._dialog.dismiss()

        form = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="120dp")
        name_field = MDTextField(text=payment["name"], hint_text="Name")
        amount_field = MDTextField(
            text=str(payment["amount"]), hint_text="Amount", input_filter="float"
        )
        form.add_widget(name_field)
        form.add_widget(amount_field)

        def do_save(*args):
            new_name = name_field.text.strip()
            try:
                new_amount = float(amount_field.text.strip())
                if new_amount <= 0:
                    raise ValueError
            except ValueError:
                self._show_message("Please enter a valid amount greater than 0.")
                return
            if not new_name:
                self._show_message("Please enter a name.")
                return
            app = MDApp.get_running_app()
            app.db.update_payment(payment["id"], name=new_name, amount=new_amount)
            edit_dialog.dismiss()
            self.refresh_list()
            self.update_total()

        edit_dialog = MDDialog(
            title="Edit Payment",
            type="custom",
            content_cls=form,
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: edit_dialog.dismiss()),
                MDRaisedButton(text="Save", on_release=do_save),
            ],
        )
        edit_dialog.open()

    def _confirm_delete(self, payment):
        self._dialog.dismiss()

        def do_delete(*args):
            app = MDApp.get_running_app()
            app.db.delete_payment(payment["id"])
            confirm_dialog.dismiss()
            self.refresh_list()
            self.update_total()

        confirm_dialog = MDDialog(
            title="Delete this payment?",
            text=f"{payment['name']} — {payment['amount']:.2f}\nThis can't be undone.",
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: confirm_dialog.dismiss()),
                MDRaisedButton(text="Delete", on_release=do_delete),
            ],
        )
        confirm_dialog.open()

    # ---------- Helper ----------

    def _show_message(self, text):
        dialog = MDDialog(
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())],
        )
        dialog.open()

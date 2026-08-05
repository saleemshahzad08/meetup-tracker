"""
utils/export.py — creates a single .zip backup containing the database
file and every receipt image, so the user has one file that captures
everything needed to restore their data.

This module has no Kivy imports so it can be tested on its own.
"""

import os
import zipfile
from datetime import datetime


def export_data(db_path, receipts_dir, export_dir):
    """
    Zips db_path and everything inside receipts_dir into a single file
    inside export_dir. Returns the full path to the created zip file.
    """
    os.makedirs(export_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"meetup_backup_{timestamp}.zip"
    zip_path = os.path.join(export_dir, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # The database file, stored at the root of the zip
        if os.path.exists(db_path):
            zf.write(db_path, arcname=os.path.basename(db_path))

        # Every file in the receipts folder, stored under receipts/
        if os.path.isdir(receipts_dir):
            for root, _dirs, files in os.walk(receipts_dir):
                for filename in files:
                    full_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(full_path, receipts_dir)
                    zf.write(full_path, arcname=os.path.join("receipts", rel_path))

    return zip_path


def get_export_dir():
    """
    Where the backup zip should be written.

    - On Android: the app's dedicated external-storage folder
      (Android/data/<package>/files/exports). This needs NO runtime
      storage permission on any Android version, and can be reached
      with a file manager or by plugging the phone into a PC via USB.
    - On desktop (Windows testing): a local ./data/exports folder,
      just so the feature is testable without a phone.
    """
    from kivy.utils import platform

    if platform == "android":
        try:
            from jnius import autoclass

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            context = PythonActivity.mActivity
            external_dir = context.getExternalFilesDir(None).getAbsolutePath()
            return os.path.join(external_dir, "exports")
        except Exception:
            # Fall back to internal app storage if the external path
            # isn't available for some reason.
            from kivymd.app import MDApp

            app = MDApp.get_running_app()
            return os.path.join(app.user_data_dir, "exports")

    return os.path.join(os.getcwd(), "data", "exports")

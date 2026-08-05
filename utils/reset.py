"""
utils/reset.py — clears receipt image files when the user chooses to
"start fresh" for a new meetup. Deletes the files inside receipts_dir,
but keeps the folder itself so the app can keep writing new receipts
into it.
"""

import os


def clear_receipts(receipts_dir):
    if not os.path.isdir(receipts_dir):
        return
    for filename in os.listdir(receipts_dir):
        file_path = os.path.join(receipts_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

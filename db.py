"""
db.py — SQLite data layer for the Meetup Fee & Expense Tracker.

All data lives in a single SQLite file. Callers pass in the path to that
file (main.py will point this at App.user_data_dir/meetup.db on real
devices, or a local ./data/meetup.db during desktop development).

No Kivy imports here on purpose — this module is pure Python/sqlite3 so
it can be unit-tested and run from a plain `python` shell without any UI
framework loaded.
"""

import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager


SCHEMA = """
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    receipt_path TEXT,
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT NOT NULL,
    amount REAL NOT NULL,
    timestamp TEXT NOT NULL
);
"""


class MeetupDB:
    """Thin wrapper around a SQLite connection to the meetup tracker DB."""

    def __init__(self, db_path):
        self.db_path = db_path
        # Make sure the parent directory exists (e.g. .../data/meetup.db)
        parent = os.path.dirname(os.path.abspath(db_path))
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        self._init_schema()

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self):
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    # ---------------------------------------------------------------
    # Payments
    # ---------------------------------------------------------------

    def add_payment(self, name, amount, receipt_path=None):
        """Insert a payment. Returns the new row's id."""
        ts = datetime.now().isoformat(timespec="seconds")
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO payments (name, amount, receipt_path, timestamp) "
                "VALUES (?, ?, ?, ?)",
                (name, amount, receipt_path, ts),
            )
            return cur.lastrowid

    def update_payment(self, payment_id, name=None, amount=None, receipt_path=None):
        """Update only the fields provided (None = leave unchanged)."""
        existing = self.get_payment(payment_id)
        if existing is None:
            raise ValueError(f"No payment with id {payment_id}")
        name = existing["name"] if name is None else name
        amount = existing["amount"] if amount is None else amount
        receipt_path = existing["receipt_path"] if receipt_path is None else receipt_path
        with self._connect() as conn:
            conn.execute(
                "UPDATE payments SET name = ?, amount = ?, receipt_path = ? WHERE id = ?",
                (name, amount, receipt_path, payment_id),
            )

    def delete_payment(self, payment_id):
        with self._connect() as conn:
            conn.execute("DELETE FROM payments WHERE id = ?", (payment_id,))

    def get_payment(self, payment_id):
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM payments WHERE id = ?", (payment_id,)
            ).fetchone()
            return dict(row) if row else None

    def list_payments(self):
        """Most recent first."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM payments ORDER BY timestamp DESC, id DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    def total_collected(self):
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) AS total FROM payments"
            ).fetchone()
            return row["total"]

    # ---------------------------------------------------------------
    # Expenses
    # ---------------------------------------------------------------

    def add_expense(self, item, amount):
        ts = datetime.now().isoformat(timespec="seconds")
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO expenses (item, amount, timestamp) VALUES (?, ?, ?)",
                (item, amount, ts),
            )
            return cur.lastrowid

    def update_expense(self, expense_id, item=None, amount=None):
        existing = self.get_expense(expense_id)
        if existing is None:
            raise ValueError(f"No expense with id {expense_id}")
        item = existing["item"] if item is None else item
        amount = existing["amount"] if amount is None else amount
        with self._connect() as conn:
            conn.execute(
                "UPDATE expenses SET item = ?, amount = ? WHERE id = ?",
                (item, amount, expense_id),
            )

    def delete_expense(self, expense_id):
        with self._connect() as conn:
            conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

    def get_expense(self, expense_id):
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM expenses WHERE id = ?", (expense_id,)
            ).fetchone()
            return dict(row) if row else None

    def list_expenses(self):
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM expenses ORDER BY timestamp DESC, id DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    def total_spent(self):
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) AS total FROM expenses"
            ).fetchone()
            return row["total"]

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------

    def balance(self):
        return self.total_collected() - self.total_spent()

    # ---------------------------------------------------------------
    # Reset (start fresh for a new meetup)
    # ---------------------------------------------------------------

    def reset_all(self):
        """Permanently deletes every payment and expense row. Does not
        touch receipt image files on disk — the caller is responsible
        for clearing those separately (see utils/reset.py)."""
        with self._connect() as conn:
            conn.execute("DELETE FROM payments")
            conn.execute("DELETE FROM expenses")
            # Reset the auto-increment counters too, so a fresh meetup
            # starts IDs back at 1 (purely cosmetic, but tidier).
            try:
                conn.execute(
                    "DELETE FROM sqlite_sequence WHERE name IN ('payments', 'expenses')"
                )
            except sqlite3.OperationalError:
                # sqlite_sequence only exists once an autoincrement
                # insert has happened; fine to ignore if it's missing.
                pass

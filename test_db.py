"""
test_db.py — quick manual sanity check for db.py.

Run with:  python test_db.py
(This is a simple smoke test, not a pytest suite — just enough to confirm
the schema and CRUD methods behave before building the UI on top of them.)
"""

import os
from db import MeetupDB

TEST_DB_PATH = "./data/test_meetup.db"


def main():
    # Start clean each run
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    db = MeetupDB(TEST_DB_PATH)

    # --- Payments ---
    p1 = db.add_payment("Ali", 500, receipt_path="receipts/ali_1.jpg")
    p2 = db.add_payment("Sara", 750, receipt_path=None)
    assert db.total_collected() == 1250, "total_collected mismatch"

    db.update_payment(p2, amount=800)
    assert db.total_collected() == 1300, "update_payment didn't recalculate total"

    payments = db.list_payments()
    assert len(payments) == 2
    print("Payments:", payments)

    db.delete_payment(p1)
    assert db.total_collected() == 800, "delete_payment didn't recalculate total"

    # --- Expenses ---
    e1 = db.add_expense("Venue rental", 300)
    e2 = db.add_expense("Snacks", 100)
    assert db.total_spent() == 400, "total_spent mismatch"

    db.update_expense(e2, amount=150)
    assert db.total_spent() == 450

    expenses = db.list_expenses()
    assert len(expenses) == 2
    print("Expenses:", expenses)

    db.delete_expense(e1)
    assert db.total_spent() == 150

    # --- Summary ---
    expected_balance = db.total_collected() - db.total_spent()
    assert db.balance() == expected_balance
    print(f"Collected: {db.total_collected()}, Spent: {db.total_spent()}, "
          f"Balance: {db.balance()}")

    print("\nAll checks passed.")


if __name__ == "__main__":
    main()

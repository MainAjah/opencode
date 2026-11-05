from app.database import get_db


def create_loan(student_id, item_id, quantity, status="BORROWED"):
    """Insert a new loan and return the stored row."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO loans (student_id, item_id, quantity, status) "
        "VALUES (?, ?, ?, ?)",
        (student_id, item_id, quantity, status),
    )
    return get_loan_by_id(cursor.lastrowid)


def get_loan_by_id(loan_id):
    """Return a single loan or None when it does not exist."""
    db = get_db()
    row = db.execute(
        "SELECT id, student_id, item_id, quantity, status, created_at "
        "FROM loans WHERE id = ?",
        (loan_id,),
    ).fetchone()
    return dict(row) if row is not None else None


def update_loan_status(loan_id, status, expected_status=None):
    """Update a loan status; return True when a row was changed.

    When expected_status is given, the update only applies if the current
    status matches, which prevents double processing.
    """
    db = get_db()
    if expected_status is None:
        cursor = db.execute(
            "UPDATE loans SET status = ? WHERE id = ?",
            (status, loan_id),
        )
    else:
        cursor = db.execute(
            "UPDATE loans SET status = ? WHERE id = ? AND status = ?",
            (status, loan_id, expected_status),
        )
    return cursor.rowcount == 1


def get_loans_by_student_id(student_id):
    """Return loan history for a student, newest first."""
    db = get_db()
    rows = db.execute(
        "SELECT id, student_id, item_id, quantity, status, created_at "
        "FROM loans WHERE student_id = ? ORDER BY created_at DESC, id DESC",
        (student_id,),
    ).fetchall()
    return [dict(row) for row in rows]

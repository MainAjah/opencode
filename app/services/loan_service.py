from app.database import get_db
from app.errors import ApiError
from app.repositories import item_repository, loan_repository
from app.validators import validate_create_loan, validate_student_id


def create_loan(data):
    """Create a loan and decrease item stock atomically."""
    student_id, item_id, quantity = validate_create_loan(data)

    if item_repository.get_item_by_id(item_id) is None:
        raise ApiError("Item not found", 404)

    db = get_db()
    try:
        if not item_repository.decrease_available_stock(item_id, quantity):
            raise ApiError("Insufficient stock", 400)

        loan = loan_repository.create_loan(student_id, item_id, quantity)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return loan


def return_loan(loan_id):
    """Mark a loan as returned and restore item stock atomically."""
    loan = loan_repository.get_loan_by_id(loan_id)
    if loan is None:
        raise ApiError("Loan not found", 404)

    if loan["status"] == "RETURNED":
        raise ApiError("Loan has already been returned", 400)
    if loan["status"] != "BORROWED":
        raise ApiError("Only borrowed loans can be returned", 400)

    db = get_db()
    try:
        updated = loan_repository.update_loan_status(
            loan_id, "RETURNED", expected_status="BORROWED"
        )
        if not updated:
            raise ApiError("Loan has already been returned", 400)

        restored = item_repository.increase_available_stock(
            loan["item_id"], loan["quantity"]
        )
        if not restored:
            raise ApiError("Item not found", 404)

        db.commit()
    except Exception:
        db.rollback()
        raise

    return loan_repository.get_loan_by_id(loan_id)


def get_student_loans(student_id):
    """Return loan history for one student."""
    student_id = validate_student_id(student_id)
    return loan_repository.get_loans_by_student_id(student_id)

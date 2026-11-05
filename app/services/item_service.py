from app.database import get_db
from app.repositories import item_repository
from app.validators import validate_create_item


def list_items():
    """Return every item with its latest stock values."""
    return item_repository.get_all_items()


def create_item(data):
    """Validate input and store a new item with its initial stock."""
    name, total_stock = validate_create_item(data)

    db = get_db()
    try:
        item = item_repository.create_item(name, total_stock, total_stock)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return item

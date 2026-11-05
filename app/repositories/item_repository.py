from app.database import get_db


def create_item(name, total_stock, available_stock):
    """Insert a new item and return the stored row."""
    db = get_db()
    cursor = db.execute(
        "INSERT INTO items (name, total_stock, available_stock) "
        "VALUES (?, ?, ?)",
        (name, total_stock, available_stock),
    )
    return get_item_by_id(cursor.lastrowid)


def get_all_items():
    """Return every item ordered by id."""
    db = get_db()
    rows = db.execute(
        "SELECT id, name, total_stock, available_stock FROM items ORDER BY id"
    ).fetchall()
    return [dict(row) for row in rows]


def get_item_by_id(item_id):
    """Return a single item or None when it does not exist."""
    db = get_db()
    row = db.execute(
        "SELECT id, name, total_stock, available_stock FROM items WHERE id = ?",
        (item_id,),
    ).fetchone()
    return dict(row) if row is not None else None


def decrease_available_stock(item_id, quantity):
    """Decrease stock only when it is sufficient; return True on success."""
    db = get_db()
    cursor = db.execute(
        "UPDATE items "
        "SET available_stock = available_stock - ? "
        "WHERE id = ? AND available_stock >= ?",
        (quantity, item_id, quantity),
    )
    return cursor.rowcount == 1


def increase_available_stock(item_id, quantity):
    """Increase stock for an existing item; return True on success."""
    db = get_db()
    cursor = db.execute(
        "UPDATE items SET available_stock = available_stock + ? WHERE id = ?",
        (quantity, item_id),
    )
    return cursor.rowcount == 1

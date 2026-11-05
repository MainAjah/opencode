from app.errors import ApiError


def _require_json_object(data):
    if not isinstance(data, dict):
        raise ApiError("Request body must be a JSON object", 400)


def validate_create_item(data):
    """Validate POST /items input and return normalized values."""
    _require_json_object(data)

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ApiError("name is required", 400)

    total_stock = data.get("total_stock")
    if isinstance(total_stock, bool) or not isinstance(total_stock, int):
        raise ApiError("total_stock must be a non-negative integer", 400)
    if total_stock < 0:
        raise ApiError("total_stock must be a non-negative integer", 400)

    return name.strip(), total_stock


def validate_create_loan(data):
    """Validate POST /loans input and return normalized values."""
    _require_json_object(data)

    student_id = data.get("student_id")
    if not isinstance(student_id, str) or not student_id.strip():
        raise ApiError("student_id is required", 400)

    item_id = data.get("item_id")
    if isinstance(item_id, bool) or not isinstance(item_id, int) or item_id <= 0:
        raise ApiError("item_id must be a positive integer", 400)

    quantity = data.get("quantity")
    if (
        isinstance(quantity, bool)
        or not isinstance(quantity, int)
        or quantity <= 0
    ):
        raise ApiError("quantity must be a positive integer", 400)

    return student_id.strip(), item_id, quantity


def validate_student_id(student_id):
    """Validate a student id taken from the URL."""
    if not isinstance(student_id, str) or not student_id.strip():
        raise ApiError("student_id is required", 400)
    return student_id.strip()

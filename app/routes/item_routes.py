from flask import Blueprint, jsonify, request

from app.services import item_service

bp = Blueprint("items", __name__, url_prefix="/items")


@bp.get("")
def list_items():
    return jsonify(item_service.list_items())


@bp.post("")
def create_item():
    item = item_service.create_item(request.get_json(silent=True))
    return jsonify(item), 201

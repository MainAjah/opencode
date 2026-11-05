from flask import Blueprint, jsonify, request

from app.services import loan_service

bp = Blueprint("loans", __name__, url_prefix="/loans")


@bp.post("")
def create_loan():
    loan = loan_service.create_loan(request.get_json(silent=True))
    return jsonify(loan), 201


@bp.put("/<int:loan_id>/return")
def return_loan(loan_id):
    loan = loan_service.return_loan(loan_id)
    return jsonify(loan), 200


@bp.get("/student/<student_id>")
def student_loans(student_id):
    return jsonify(loan_service.get_student_loans(student_id))

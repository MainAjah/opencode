from tests.base import ApiTestCase


class LoanApiTests(ApiTestCase):
    def setUp(self):
        super().setUp()
        self.item = self.create_item(total_stock=10)

    def post_loan(self, student_id="20240001", item_id=None, quantity=1):
        if item_id is None:
            item_id = self.item["id"]
        return self.client.post(
            "/loans",
            json={
                "student_id": student_id,
                "item_id": item_id,
                "quantity": quantity,
            },
        )

    def get_stock(self, item_id=None):
        if item_id is None:
            item_id = self.item["id"]
        items = {item["id"]: item for item in self.get_items()}
        return items[item_id]["available_stock"]

    def test_create_loan_with_valid_data(self):
        response = self.post_loan(quantity=3)

        self.assertEqual(response.status_code, 201)
        loan = response.get_json()
        self.assertEqual(loan["student_id"], "20240001")
        self.assertEqual(loan["item_id"], self.item["id"])
        self.assertEqual(loan["quantity"], 3)
        self.assertEqual(loan["status"], "BORROWED")
        self.assertTrue(loan["created_at"])
        self.assertEqual(self.get_stock(), 7)

    def test_loan_rejected_when_stock_is_insufficient(self):
        response = self.post_loan(quantity=11)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Insufficient stock")
        self.assertEqual(self.get_stock(), 10)

    def test_failed_loan_does_not_create_transaction(self):
        self.post_loan(quantity=11)

        history = self.client.get("/loans/student/20240001")
        self.assertEqual(history.status_code, 200)
        self.assertEqual(history.get_json(), [])

    def test_loan_with_unknown_item_returns_404(self):
        response = self.post_loan(item_id=999, quantity=1)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Item not found")

    def test_loan_with_invalid_quantity(self):
        for quantity in (0, -1, 1.5, "2", True, None):
            with self.subTest(quantity=quantity):
                response = self.post_loan(quantity=quantity)
                self.assertEqual(response.status_code, 400)

        self.assertEqual(self.get_stock(), 10)

    def test_loan_without_required_fields(self):
        response = self.client.post(
            "/loans",
            json={"item_id": self.item["id"], "quantity": 1},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("student_id", response.get_json()["error"])

    def test_return_loan_with_valid_data(self):
        loan = self.post_loan(quantity=2).get_json()

        response = self.client.put(f"/loans/{loan['id']}/return")

        self.assertEqual(response.status_code, 200)
        returned = response.get_json()
        self.assertEqual(returned["status"], "RETURNED")
        self.assertEqual(self.get_stock(), 10)

    def test_return_unknown_loan_returns_404(self):
        response = self.client.put("/loans/999/return")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Loan not found")

    def test_loan_cannot_be_returned_twice(self):
        loan = self.post_loan(quantity=2).get_json()

        first = self.client.put(f"/loans/{loan['id']}/return")
        second = self.client.put(f"/loans/{loan['id']}/return")

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 400)
        self.assertEqual(
            second.get_json()["error"], "Loan has already been returned"
        )
        self.assertEqual(self.get_stock(), 10)

    def test_student_history_only_contains_requested_student(self):
        self.post_loan(student_id="20240001", quantity=2)
        self.post_loan(student_id="20240002", quantity=1)

        response = self.client.get("/loans/student/20240001")

        self.assertEqual(response.status_code, 200)
        history = response.get_json()
        self.assertEqual(len(history), 1)
        self.assertTrue(
            all(loan["student_id"] == "20240001" for loan in history)
        )

    def test_student_history_is_empty_for_unknown_student(self):
        response = self.client.get("/loans/student/00000000")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_stock_stays_consistent_after_multiple_transactions(self):
        first = self.post_loan(quantity=2).get_json()
        second = self.post_loan(quantity=3).get_json()
        self.assertEqual(self.get_stock(), 5)

        self.client.put(f"/loans/{first['id']}/return")
        self.assertEqual(self.get_stock(), 7)

        self.client.put(f"/loans/{second['id']}/return")
        self.assertEqual(self.get_stock(), 10)

    def test_unknown_route_returns_json_error(self):
        response = self.client.get("/does-not-exist")

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

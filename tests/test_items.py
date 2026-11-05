from tests.base import ApiTestCase


class ItemApiTests(ApiTestCase):
    def test_get_items_when_database_is_empty(self):
        response = self.client.get("/items")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_item_with_valid_data(self):
        response = self.client.post(
            "/items",
            json={"name": "Multimeter", "total_stock": 10},
        )

        self.assertEqual(response.status_code, 201)
        item = response.get_json()
        self.assertEqual(item["name"], "Multimeter")
        self.assertEqual(item["total_stock"], 10)
        self.assertEqual(item["available_stock"], 10)
        self.assertIn("id", item)

    def test_create_item_without_name(self):
        response = self.client.post(
            "/items",
            json={"total_stock": 10},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_create_item_with_blank_name(self):
        response = self.client.post(
            "/items",
            json={"name": "   ", "total_stock": 10},
        )

        self.assertEqual(response.status_code, 400)

    def test_create_item_with_negative_stock(self):
        response = self.client.post(
            "/items",
            json={"name": "Multimeter", "total_stock": -1},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.get_items(), [])

    def test_create_item_with_non_integer_stock(self):
        for total_stock in (1.5, "10", None, True):
            with self.subTest(total_stock=total_stock):
                response = self.client.post(
                    "/items",
                    json={"name": "Multimeter", "total_stock": total_stock},
                )
                self.assertEqual(response.status_code, 400)

    def test_create_item_with_invalid_json(self):
        response = self.client.post(
            "/items",
            data="not-json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

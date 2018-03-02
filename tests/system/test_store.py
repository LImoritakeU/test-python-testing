import json

from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/test')

                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(
                    {"id": 1, "name": "test", "items": []},
                    json.loads(resp.data)
                )

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                resp = client.post('/store/test')
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual(
                    {"message": "A store with name 'test' already exists."},
                    json.loads(resp.data),
                )

    def test_delete_store(self):
        with self.app() as cli:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = cli.delete('/store/test')

                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(
                    {"message": "Store deleted"},
                    json.loads(resp.data),
                )

    def test_find_store(self):
        with self.app() as cli:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = cli.get('/store/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(
                    {"id": 1, "name": 'test', 'items': []},
                    json.loads(resp.data)
                )

    def test_store_not_found(self):
       with self.app() as cli:
            with self.app_context():
                resp = cli.get('/store/test')

                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual(
                    {"message": "Store not found"},
                    json.loads(resp.data)
                )

    def test_store_found_with_items(self):
        with self.app() as cli:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = cli.get('/store/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(
                    {"id": 1, "name": "test", "items": [{"name": "test", "price": 19.99},]},
                    json.loads(resp.data)
                )


    def test_store_list(self):
        with self.app() as cli:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = cli.get('/stores')
                self.assertDictEqual(
                    {'stores': [
                        {"id": 1, 'name': 'test', 'items': []}
                    ]},
                    json.loads(resp.data)
                )


    def test_store_list_with_items(self):
        with self.app() as cli:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                resp = cli.get('/stores')
                self.assertDictEqual(
                    {'stores': [
                        {
                            "id": 1,
                            "name": "test",
                            "items": [{"name": "test", "price": 19.99},]
                        }
                    ]},
                    json.loads(resp.data)
                )



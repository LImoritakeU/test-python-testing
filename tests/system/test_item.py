from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):

    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as cli:
            with self.app_context():
                UserModel("test", "1234").save_to_db()

                resp = cli.post('/auth',
                                data=json.dumps({'username': 'test', 'password': '1234'}),
                                headers={'Content-Type': 'application/json'})
                token = json.loads(resp.data)['access_token']
                self.auth_token = "JWT {}".format(token)

    def test_get_item_no_auth(self):
        with self.app() as cli:
            with self.app_context():
                resp = cli.get('/item/test')

                self.assertEqual(resp.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as cli:
            with self.app_context():
                resp = cli.get('/item/test',
                               headers={"Authorization": self.auth_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as cli:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = cli.get('/item/test',
                               headers={"Authorization": self.auth_token})
                self.assertEqual(resp.status_code, 200)

    def test_delete_item(self):
        with self.app() as cli:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = cli.delete('/item/test')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {"message": "Item deleted"})

    def test_create_item(self):
        with self.app() as cli:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = cli.post('/item/test',
                                data={"price": 19.99, "store_id": 1})
                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name('test'))

    def test_create_duplicate_item(self):
        with self.app() as cli:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = cli.post('/item/test',
                                data={"price": 19.99, "store_id": 1})
                self.assertEqual(resp.status_code, 400)

    def test_put_item(self):
        with self.app() as cli:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = cli.put('/item/test',
                               data={"price": 19.99, "store_id": 1})
                self.assertEqual(resp.status_code, 200)
                self.assertIsNotNone(ItemModel.find_by_name('test'))

    def test_put_update_item(self):
        with self.app() as cli:
            with self.app_context():
                StoreModel('test').save_to_db()

                resp = cli.put('/item/test',
                               data={"price": 20.99, "store_id": 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(json.loads(resp.data)['price'], 20.99)

    def test_item_list(self):
        pass



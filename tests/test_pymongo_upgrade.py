"""Run with chapter 9 requirements: python -m unittest discover -s tests -p test_pymongo_upgrade.py -v."""
import runpy
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

import pymongo
from bson import BSON
from pymongo.errors import InvalidURI
from pymongo.uri_parser import parse_uri


class PyMongoUpgradeTests(unittest.TestCase):
    def test_encoded_host_delimiters_cannot_inject_seeds(self):
        """GHSA-vp6j-j7w5-5xjj: parse without contacting a server."""
        for host in ['trusted%2Cattacker:27017', 'trusted%3A27017', 'trusted%2cattacker:27017']:
            with self.subTest(host=host), self.assertRaises(InvalidURI):
                parse_uri('mongodb://' + host + '/')

    def test_normal_local_uri_and_bson_round_trip(self):
        self.assertEqual(parse_uri('mongodb://localhost:27017/')['nodelist'], [('localhost', 27017)])
        record = {'name': 'Example', 'height': '170', 'weight': '65'}
        self.assertEqual(BSON.encode(record).decode(), record)
        self.assertGreaterEqual(tuple(map(int, pymongo.version.split('.')[:3])), (4, 18, 2))

    def test_teaching_scripts_keep_basic_driver_calls(self):
        scripts = Path(__file__).resolve().parents[1] / 'dj4ch09' / 'dj4ch09' / 'mongo-db'
        cases = {
            'listdb.py': [],
            'listdata.py': [],
            'insertdata.py': ['Example', '170', '65', ''],
            'deldata.py': ['Example', ''],
        }
        for filename, answers in cases.items():
            with self.subTest(script=filename):
                client = MagicMock()
                collection = client.__getitem__.return_value.__getitem__.return_value
                collection.find.return_value = []
                with patch('pymongo.MongoClient', return_value=client) as constructor, \
                        patch('builtins.input', side_effect=answers), patch('builtins.print'):
                    runpy.run_path(str(scripts / filename), run_name='__main__')
                constructor.assert_called_once_with('mongodb://localhost:27017/')
                if filename == 'insertdata.py':
                    collection.insert_one.assert_called_once_with(
                        {'name': 'Example', 'height': '170', 'weight': '65'})
                elif filename == 'deldata.py':
                    collection.delete_one.assert_called_once_with({'name': 'Example'})
                elif filename == 'listdb.py':
                    client.list_database_names.assert_called_once_with()
                else:
                    collection.find.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()

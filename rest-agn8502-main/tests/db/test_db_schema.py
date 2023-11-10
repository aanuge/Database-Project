import unittest
from src.db.chat_db import *
from src.db.swen344_db_utils import connect
from tests.test_utils import *


class TestDBSchema(unittest.TestCase):

    def test_rebuild_tables(self):
        """Rebuild the tables"""
        rebuild_tables()
        assert_sql_count(self, "SELECT * FROM users", 9)

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        rebuild_tables()
        rebuild_tables()
        assert_sql_count(self, "SELECT * FROM users", 9)

    def test_seed_data_works(self):
        """Attempt to insert the seed data"""
        rebuild_tables()
        assert_sql_count(self, "SELECT * FROM users", 9)

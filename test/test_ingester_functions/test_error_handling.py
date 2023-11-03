"""Tests for ingestion_handler error handling"""
import unittest
from unittest import mock
import os
from ingester import ingestion_handler


@mock.patch.dict(os.environ, {"DB_USER": 'test', "DB_NAME": 'test',
                              "DB_PORT": "123", "DB_HOST": 'test',
                              "DB_PASSWORD": '123'})
class myTestCase(unittest.TestCase):
    def test_raises_pg8000_errors(self):
        """Test that ingestion_handler() logs pg8000 errors for connection and
        database errors
        """
        ingestion_handler("", "")
        with self.assertLogs('MyLogger', level='ERROR') as cm:
            ingestion_handler("", "")
        self.assertEqual(cm.output,
                         ["ERROR:MyLogger:Critical pg8000 error: "
                          "Can't create a connection to host test "
                          "and port 123 (timeout is None and "
                          "source_address is None)."])

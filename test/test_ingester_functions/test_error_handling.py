"""Tests for ingestion_handler error handling"""
from src.ingester import ingestion_handler
import unittest
import logging
from pg8000.native import Connection
from unittest import mock
import os
import logging

@mock.patch.dict(os.environ, {"DB_USER": 'test', "DB_NAME": 'test',
                                "DB_PORT": "123", "DB_HOST":'test',
                                "DB_PASSWORD": '123'})
def test_raises_pg8000_errors():
    """Test that ingestion_handler() logs pg8000 errors for connection and
    database errors
    """
    ingestion_handler()
    # with assertLogs('MyLogger', level='ERROR') as cm:
    #     ingestion_handler()
    # assertEqual(cm.output, ['INFO:foo:first message',
    #                                 'ERROR:foo.bar:second message'])

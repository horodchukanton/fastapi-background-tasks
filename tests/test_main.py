from datetime import datetime

from pytest import fixture

from fastapi.testclient import TestClient
from fastapi_background_tasks_test.main import app


class Clock:
    _timestamp = None

    def __enter__(self):
        self._timestamp = datetime.now()
        return self

    def __exit__(self, *args):
        pass

    def elapsed(self):
        return (datetime.now() - self._timestamp).seconds


class TestMain:

    @fixture(name="test_client")
    def fastapi_test_client(self):
        return TestClient(app)

    @fixture
    def clock(self):
        return Clock()

    def test_sync(self, test_client, clock):
        with clock as cl:
            test_client.get('/sync')
            assert cl.elapsed() < 1

    def test_async(self, test_client, clock):
        with clock as cl:
            test_client.get('/async')
            assert cl.elapsed() < 1

    def test_async_with_sync(self, test_client, clock):
        with clock as cl:
            test_client.get('/async_sync')
            assert cl.elapsed() < 1

    def test_async_with_async_lock(self, test_client, clock):
        with clock as cl:
            test_client.get('/async_with_async_lock')
            assert cl.elapsed() < 1

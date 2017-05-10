import asyncio
import uvloop
import pytest

from aiohttp.test_utils import TestClient


@pytest.fixture
def loop(request):
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(None)

    yield loop

    loop.stop()
    loop.run_forever()
    loop.close()
    asyncio.set_event_loop(None)


@pytest.fixture
def test_client(loop):
    clients = []

    @asyncio.coroutine
    def go(__param, *args, **kwargs):
        __param = __param(loop, *args, **kwargs)
        client = TestClient(__param, loop=loop)

        yield from client.start_server()
        clients.append(client)
        return client

    yield go

    @asyncio.coroutine
    def finalize():
        while clients:
            yield from clients.pop().close()

    loop.run_until_complete(finalize())

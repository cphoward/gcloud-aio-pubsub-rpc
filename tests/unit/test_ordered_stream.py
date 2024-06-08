# import asyncio
import unittest
import pytest
from pubsub_rpc.ordered_stream import AsyncOrderedStream


# class TestAsyncOrderedStream(unittest.TestCase):

async def test_single_item():
    stream = AsyncOrderedStream()
    await stream.add('item1', 0, 'sender1')
    result = await stream.__anext__()
    assert result == 'item1'


async def test_multiple_items_in_order() -> None:
    stream = AsyncOrderedStream()
    await stream.add('item1', 0, 'sender1')
    await stream.add('item2', 1, 'sender1')
    results = []
    async for item in stream:
        results.append(item)
        if len(results) == 2:
            break
    assert results == ['item1', 'item2']


async def test_items_out_of_order() -> None:
    stream = AsyncOrderedStream()
    await stream.add('item2', 2, 'sender1')
    await stream.add('item1', 1, 'sender1')
    await stream.add('item0', 0, 'sender1')
    results = []
    async for item in stream:
        results.append(item)
        if len(results) == 3:
            break
    assert results == ['item0', 'item1', 'item2']


async def test_wrong_sender() -> None:
    stream = AsyncOrderedStream()
    await stream.add('item1', 0, 'sender1')
    await stream.add('item2', 1, 'sender2')
    result = await stream.__anext__()
    assert result == 'item1'
    await stream.signal_end_of_stream(1, 'sender1')

    with pytest.raises(StopAsyncIteration):
        # Should raise because 'item2' from 'sender2' is ignored
        await stream.__anext__()


async def test_wrong_sender_with_eos_out_of_order() -> None:
    stream = AsyncOrderedStream()
    await stream.signal_end_of_stream(1, 'sender1')
    await stream.add('item1', 0, 'sender1')
    await stream.add('item2', 1, 'sender2')
    result = await stream.__anext__()
    assert result == 'item1'

    with pytest.raises(StopAsyncIteration):
        # Should raise because 'item2' from 'sender2' is ignored
        await stream.__anext__()

    # async def test_timeout(self):
    #     stream = AsyncOrderedStream(timeout=1)
    #     start_time = asyncio.get_event_loop().time()
    #     with self.assertRaises(asyncio.TimeoutError):
    #         await stream.__anext__()
    #     end_time = asyncio.get_event_loop().time()
    #     self.assertTrue(end_time - start_time >= 1)


# You can use this to run the tests from the command line
if __name__ == '__main__':
    unittest.main()

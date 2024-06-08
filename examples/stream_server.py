import asyncio
import logging
import typer

# from pubsub_rpc import PubSubRPCStreamServer
from pubsub_rpc import PubSubRPCServer

from gcloud.aio.pubsub import PubsubMessage
from gcloud.aio.pubsub import SubscriberMessage

from collections.abc import AsyncIterator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = typer.Typer()


class RPCStreamServer(PubSubRPCServer):
    async def process_stream_message(
            self, message: SubscriberMessage) -> AsyncIterator[PubsubMessage]:
        """The user-defined, per-message stream transform to apply to a message"""
        data = message.data.decode()
        for index in range(1000):
            # Simulate something time consuming
            await asyncio.sleep(0.05)
            yield PubsubMessage(f'{data} message {index} of 999',
                                **message.attributes)

    async def process_message(
            self, message: SubscriberMessage) -> list[PubsubMessage]:
        """The user-defined, per-message transform to apply to a message"""
        return [PubsubMessage(message.data,
                              **message.attributes)]


async def _main(project_id: str,
                input_subscription_name: str,
                input_topic: str,
                output_topic: str) -> None:
    manager = RPCStreamServer(project_id, input_subscription_name, input_topic, output_topic)
    await manager.initialize()
    await manager.startup()
    try:
        await manager.producer
    except asyncio.CancelledError:
        pass
    except Exception:
        logger.exception('Exception caught on shutdown')
    finally:
        await manager.cleanup()


@app.command()
def main(project_id: str = typer.Argument(...),
         input_subscription_name: str = typer.Argument(...), 
         input_topic: str = typer.Argument(...), 
         output_topic: str = typer.Argument(...)) -> None:
    asyncio.run(_main(project_id, input_subscription_name, input_topic, output_topic))


if __name__ == '__main__':
    typer.run(main)

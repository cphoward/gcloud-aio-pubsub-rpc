import asyncio
import logging
import typer
from pubsub_rpc import PubSubRPCClient

app = typer.Typer()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def _main(project_id: str,
                input_topic: str,
                output_topic: str) -> None:
    client = PubSubRPCClient(project_id, input_topic, output_topic)
    await client.initialize()
    await client.startup()
    print('Submitting message')
    try:
        stream = await client.submit('Stream example', timeout=61, stream=True)
        async for chunk in stream:
            print('user-space chunk', chunk)
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        pass
    except Exception:
        logger.exception('Exception caught on shutdown')
    finally:
        await client.cleanup()


@app.command()
def main(project_id: str = typer.Argument(...),
         input_topic: str = typer.Argument(...),
         output_topic: str = typer.Argument(...)) -> None:
    asyncio.run(_main(project_id, input_topic, output_topic))


if __name__ == '__main__':
    typer.run(main)

import asyncio
import logging

from pubsub_rpc import PubSubRPCClient

app = typer.Typer()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def _main(project_id: str,
                input_topic: str,
                output_topic: str) -> None:
    client = PubSubRPCClient(project_id, input_topic, output_topic)
    client = PubSubRPCClient(
    await client.initialize()
    await client.startup()
    print('Submitting message')
    gathered_tasks = asyncio.gather(
        *[client.submit(f'Hello World {i}') for i in range(100)]
    )
    try:
        # await client.worker
        await gathered_tasks
        logger.info('All tasks completed')
        # await client.submit('Hello World 1')
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        pass
    except Exception:
        logger.exception('Exception caught on shutdown')
    finally:
        logging.info('shutting down')
        # await client.shutdown()
        logging.info('cleaning up')
        await client.cleanup()
        logging.info('exiting')

@app.command()
def main(project_id: str = typer.Argument(...),
         input_topic: str = typer.Argument(...),
         output_topic: str = typer.Argument(...)) -> None:
    asyncio.run(_main(project_id, input_topic, output_topic))
        
if __name__ == '__main__':
    asyncio.run(main())

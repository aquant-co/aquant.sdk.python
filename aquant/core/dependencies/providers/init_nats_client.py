from aquant.infra.nats import NatsClient


async def init_nats_client(logger, servers, user, password):
    nats_client = NatsClient(
        logger=logger, servers=servers, user=user, password=password
    )
    await nats_client.connect()
    yield nats_client
    await nats_client.close()

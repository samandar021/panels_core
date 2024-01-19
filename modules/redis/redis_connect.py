from redis import asyncio as aioredis

from modules.config_manager.config_manager import get_configs

config_redis = get_configs()['common']['redis']


async def connect_redis():
    host = config_redis['connection']['host']
    port = config_redis['connection']['port']
    url = f'redis://{host}:{port}'

    redis = await aioredis.from_url(url, db=1)
    return redis

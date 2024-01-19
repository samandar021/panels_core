from modules.redis.redis_connect import connect_redis


async def set_ip_in_redis(client_ip: str) -> None:
    redis = await connect_redis()
    count_request_ip = await redis.get(client_ip)
    if count_request_ip is None:
        count_request_ip = 0
    count_request_ip = int(count_request_ip) + 1
    await redis.set(client_ip, value=count_request_ip, ex=86400)


async def get_ip_in_redis(client_ip: str) -> int:
    redis = await connect_redis()
    count_request_ip = await redis.get(client_ip)
    if count_request_ip is None:
        count_request_ip = 0
    return int(count_request_ip)


async def delete_ip_in_redis(client_ip: str) -> None:
    redis = await connect_redis()
    await redis.delete(client_ip)

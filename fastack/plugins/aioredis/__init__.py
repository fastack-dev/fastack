import aioredis
from fastapi import Request

from fastack import Fastack


def setup(app: Fastack):
    pass


async def connect(request: Request, cache: str) -> aioredis.Redis:
    conn_data = request.state.settings.CACHES[cache]
    return await aioredis.from_url(**conn_data)

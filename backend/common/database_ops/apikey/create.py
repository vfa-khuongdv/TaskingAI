from common.models import Apikey
from .get import get_apikey
from .list import get_apikey_total
from common.error import raise_http_error, ErrorCode


async def create_apikey(postgres_conn, name: str, max_count: int):
    new_id = Apikey.generate_random_id()
    new_apikey = Apikey.generate_random_apikey(new_id)

    # 1. select the number of apikeys in the project
    if max_count > 0:
        total = await get_apikey_total(postgres_conn)
        if total >= max_count:
            raise_http_error(
                ErrorCode.RESOURCE_LIMIT_REACHED,
                message=f"The number of API Keys has reached the maximum limit of {max_count}.",
            )

    # 2. insert the new apikey
    await postgres_conn.execute(
        """
        INSERT INTO apikey (
            apikey_id, apikey, name
        ) VALUES ($1, $2, $3);
    """,
        new_id,
        new_apikey,
        name,
    )

    # 3. get and cache the new apikey
    apikey: Apikey = await get_apikey(postgres_conn, new_id)

    return apikey

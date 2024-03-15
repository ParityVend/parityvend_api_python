from parityvend_api import AsyncParityVendAPI, env_get
import asyncio


async def main():
    parityvend = AsyncParityVendAPI(env_get("PARITYVEND_SECRET_KEY", ""))
    print(await parityvend.get_quota_info())
    await parityvend.deinit()  # close the session when you finish working


asyncio.get_event_loop().run_until_complete(main())

"""

Example "Hello World" (async)
Gets your ParityVend account quota information and prints it.

--- Expected output ---
Response({'status': 'ok', 'quota_limit': 1000000, 'quota_used': 3121, 'quota_left': 996879})

"""

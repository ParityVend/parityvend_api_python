from parityvend_api import ParityVendAPI, env_get

parityvend = ParityVendAPI(env_get("PARITYVEND_SECRET_KEY", ""))
print(parityvend.get_quota_info())

"""

Example "Hello World" (sync)
Gets your ParityVend account quota information and prints it.

--- Expected output ---
Response({'status': 'ok', 'quota_limit': 1000000, 'quota_used': 3121, 'quota_left': 996879})

"""

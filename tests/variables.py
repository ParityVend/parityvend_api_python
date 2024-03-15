from parityvend_api import env_get

secret_key = env_get("parityvend_secret_key", "")
secret_key_free = env_get("parityvend_secret_key_free", "")
invalid_secret_key = "some-invalid-secret-key"

ipv4_zimbabwe = "102.128.79.255"
ipv6_zimbabwe = "2c0f:f758::"
ipv4_switzerland = "102.129.143.0"

ipv4_venezuela = "190.206.117.0"

ipv6_vpn_cn = "2001:251::"
google_ipv4 = "8.8.8.8"

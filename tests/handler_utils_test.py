from ipaddress import IPv4Address, IPv6Address
from parityvend_api import ParityVendAPI


def test_auto_convert_ip():
    assert ParityVendAPI.auto_convert_ip("8.8.8.8") == "8.8.8.8"
    assert ParityVendAPI.auto_convert_ip(b"8.8.8.8") == "8.8.8.8"
    assert ParityVendAPI.auto_convert_ip(IPv4Address("8.8.8.8")) == "8.8.8.8"

    assert ParityVendAPI.auto_convert_ip("2c0f:f758::") == "2c0f:f758::"
    assert ParityVendAPI.auto_convert_ip(b"2c0f:f758::") == "2c0f:f758::"

    assert (
        ParityVendAPI.auto_convert_ip(
            IPv6Address("2c0f:f758:0000:0000:0000:0000:0000:0000")
        )
        == "2c0f:f758:0000:0000:0000:0000:0000:0000"
    )

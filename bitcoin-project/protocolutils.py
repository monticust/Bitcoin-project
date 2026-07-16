from hashlib import sha256
from time import time
import os


def inet_addr(ip_address):
    services = bytearray.fromhex("01 00 00 00 00 00 00 00")

    host_prefix = bytearray.fromhex(
        "00 00 00 00 00 00 00 00 00 00 FF FF"
    )

    host_bytes = bytes(
        int(part) for part in ip_address.split(".")
    )

    port = 8333
    port_bytes = port.to_bytes(2, "big")

    return services + host_prefix + host_bytes + port_bytes


def checksum(payload):
    first_hash = sha256(payload).digest()
    second_hash = sha256(first_hash).digest()

    return second_hash[:4]


def parse_header(data):
    magic = data[:4]

    command = (
        data[4:16]
        .rstrip(b"\x00")
        .decode()
    )

    payload_length = int.from_bytes(
        data[16:20],
        "little"
    )

    checksum_bytes = data[20:24]

    payload = data[24:24 + payload_length]

    return (
        magic,
        command,
        payload_length,
        checksum_bytes,
        payload,
    )


def generate_random():
    return os.urandom(8)


def version_command(host):
    version = 70015
    version_bytes = version.to_bytes(4, "little")

    services = bytearray.fromhex(
        "01 00 00 00 00 00 00 00"
    )

    timestamp = int(time())
    timestamp_bytes = timestamp.to_bytes(8, "little")

    receiver_address = inet_addr(host)
    sender_address = inet_addr("10.0.0.1")

    node_id = generate_random()

    sub_version_string = "/Satoshi:0.7.2/"
    sub_version_length = len(sub_version_string)

    sub_version_length_bytes = (
        sub_version_length.to_bytes(1, "little")
    )

    sub_version_bytes = (
        sub_version_length_bytes
        + sub_version_string.encode()
    )

    last_block = 0
    last_block_bytes = last_block.to_bytes(4, "little")

    relay = 0
    relay_bytes = relay.to_bytes(1, "little")

    payload = (
        version_bytes
        + services
        + timestamp_bytes
        + receiver_address
        + sender_address
        + node_id
        + sub_version_bytes
        + last_block_bytes
        + relay_bytes
    )

    return payload


def bitcoin_message(command, payload):
    magic_number = bytearray.fromhex("F9 BE B4 D9")

    command_bytes = command.encode()

    if len(command_bytes) > 12:
        raise ValueError(
            "Bitcoin commands cannot exceed 12 bytes"
        )

    command_bytes += b"\x00" * (12 - len(command_bytes))

    payload_length_bytes = len(payload).to_bytes(
        4,
        "little"
    )

    checksum_bytes = checksum(payload)

    message = (
        magic_number
        + command_bytes
        + payload_length_bytes
        + checksum_bytes
        + payload
    )

    return message
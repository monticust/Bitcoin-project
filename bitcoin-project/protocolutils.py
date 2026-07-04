from hashlib import sha256


def inet_addr(ip_address):
    services = bytearray.fromhex("01 00 00 00 00 00 00 00")
    host_prefix = bytearray.fromhex("00 00 00 00 00 00 00 00 00 00 FF FF")
    host_bytes = bytes(int(part) for part in ip_address.split("."))
    port = 8333
    port_bytes = port.to_bytes(2, "big")

    return services + host_prefix + host_bytes + port_bytes


def checksum(payload):
    h1 = sha256()
    h1.update(payload)
    first_hash = h1.digest()

    h2 = sha256()
    h2.update(first_hash)
    finished_hash = h2.digest()

    return finished_hash[:4]


def parse_header(data):
    magic = data[:4]
    command = data[4:16].rstrip(b"\x00").decode()
    payload_length = int.from_bytes(data[16:20], "little")
    checksum_bytes = data[20:24]
    payload = data[24:24 + payload_length]

    return magic, command, payload_length, checksum_bytes, payload
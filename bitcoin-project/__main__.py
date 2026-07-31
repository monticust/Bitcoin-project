from socketutils import send_message

from hexutils import hexprint
from protocolutils import (
    bitcoin_message,
    parse_header,
    version_command,
)


HOST = "34.146.117.255"
PORT = 8333




payload = version_command(HOST)
message = bitcoin_message("version", payload)

print("sending message")
hexprint(message)

response = send_message(HOST, PORT, message)

print("response from node")
hexprint(response)


magic, command, payload_length, checksum_bytes, version_payload = (
    parse_header(response)
)

print("magic:", magic.hex())
print("command:", command)
print("payload length:", payload_length)
print("checksum:", checksum_bytes.hex())


if command == "version":
    payload = version_payload

   

if relay_position < len(payload):
        relay = payload[relay_position]
    else:
        relay = None

    print("version:", version)
    print("services:", services)
    print("timestamp:", timestamp)
    print("receiver address:", addr_recv.hex())
    print("sender address:", addr_from.hex())
    print("nonce:", nonce.hex())
    print("user agent:", user_agent)
    print("start height:", start_height)
    print("relay:", relay)
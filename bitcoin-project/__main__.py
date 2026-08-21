from socketutils import send_message

from hexutils import hexprint
from protocolutils import (
    bitcoin_message,
    parse_header,
    version_command,
    parse_version_command,
    parse_messages
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

# todo i need a function to split response into an array of messages, which will be an array of byte arrays.
# messages = parse_messages(response)

messages = parse_messages(response)

for message in messages:
    magic, command, payload_length, checksum_bytes, payload = (
        parse_header(message)
    )

    if command == "version":
        parse_version_command(payload)

    elif command == "verack":
        print("Handshake acknowledged")
# here ill be using messages[0]







print("magic:", magic.hex())
print("command:", command)
print("payload length:", payload_length)
print("checksum:", checksum_bytes.hex())

if command == "version":

    version, services, timestamp, addr_recv, addr_from, nonce, user_agent, start_height, relay = (
        parse_version_command(version_payload)
    )

    print("version:", version)
    print("services:", services)
    print("timestamp:", timestamp)
    print("receiver address:", addr_recv.hex())
    print("sender address:", addr_from.hex())
    print("nonce:", nonce.hex())
    print("user agent:", user_agent)
    print("start height:", start_height)
    print("relay:", relay)
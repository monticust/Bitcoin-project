from socketutils import send_message_and_return_response
from protocol_model import Message
from hexutils import hexprint

from protocolutils import (
    bitcoin_message,
    version_command,
    parse_messages,
)


HOST = "34.146.117.255"
PORT = 8333




payload = version_command(HOST)
message = bitcoin_message("version", payload)

print("sending message")
hexprint(message)

response = send_message_and_return_response(HOST, PORT, message)

print("response from node")
hexprint(response)



messages = parse_messages(response)

for message in messages:
    message_object = Message.from_bytes(message)
    command_object = message_object.to_command()
    command_object.print() 









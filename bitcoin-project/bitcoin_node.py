from protocol_model import VersionCommand, Message

PORT = 8333


class BitcoinNode:
    def __init__(self,host):
        self.host = host

    def initiate_communication(self):
        command = VersionCommand.from_host(self.host)
        message = Message.from_command(command)
        responses = message.send(self.host, PORT)
        for response in responses:
            command_object = response.to_command()
            command_object.print()



from protocol_model import Message, BaseCommand, VersionCommand
 

HOST = "34.146.117.255"
PORT = 8333




command: BaseCommand = VersionCommand.from_host(HOST)

message: Message = Message.from_command(command)

responses: list[Message] = message.send(HOST,PORT)



for response in responses:
     command_object = response.to_command()
     command_object.print()








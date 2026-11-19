from bitcoin_node import BitcoinNode
 

HOST = "34.146.117.255"

#The business of this application is beginning communication with bitcoin nodes
node: BitcoinNode = BitcoinNode(HOST)
node.initiate_communication()


# command: BaseCommand = VersionCommand.from_host(HOST)

# message: Message = Message.from_command(command)

# responses: list[Message] = message.send(HOST,PORT)



# for response in responses:
#      command_object : BaseCommand = response.to_command()
#      command_object.print()








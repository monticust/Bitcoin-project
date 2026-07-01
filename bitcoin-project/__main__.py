import socket
import binascii
from time import time
import os
from hashlib import sha256

HOST = "34.146.117.255"  #  seed.bitcoin.jonasschnelli.ch (dnsseed.bluematt.me 147.236.214.146 : didnt "recieved b"")
PORT = 8333 # The port used by the server

# message = bytes([0xf9,0xbe,0xb4,0xd9,0x76,0x65,0x72,0x73,0x69,0x6f,0x6e,0x00,0x00,0x00,0x00,
# 0x00,0x64,0x00,0x00,0x00,0x35,0x8d,0x49,0x32,0x62,0xea,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,
# 0x00,0x00,0x11,0xb2,0xd0,0x50,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
# 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xff,0xff,0x00,0x00,0x00,0x00,0x00,0x00,
# 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
# 0xff,0xff,0x00,0x00,0x00,0x00,0x00,0x00,0x3b,0x2e,0xb3,0x5d,0x8c,0xe6,0x17,0x65,0x0f,0x2f,0x53,
# 0x61,0x74,0x6f,0x73,0x68,0x69,0x3a,0x30,0x2e,0x37,0x2e,0x32,0x2f,0xc0,0x3e,0x03,0x00,])

#Message Header:
#F9 BE B4 D9                                      magic number
#76 65 72 73 69 6F 6E 00 00 00 00 00              version command
                                                  #payload length 
                                                  #checksum

#Version message:
#7F 11 01 00                                      -protocol version
#01 00 00 00 00 00 00 00                          - 1 (NODE_NETWORK services)
#                                                 -hex(timestamp_to_be_converted)
#                                                 -reciepient address function
#                                                 - Sender address info - see Network Address
#                                                 - Node ID
#                                                 - "/Satoshi:0.7.2/" sub-version string (string is 15 bytes long)
#00 00 00 00                                      - Last block sending node has is block #212672
#00                                               - relay



# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     result = s.sendall(message)
#     print(result)  
#     data = s.recv(1024)

# print(f"Received {data!r}")

def hex(timestamp_to_be_converted):
   return

def inet_addr(ip_address):
    services = bytearray.fromhex("01 00 00 00 00 00 00 00")

    host_prefix = bytearray.fromhex("00 00 00 00 00 00 00 00 00 00 FF FF")
    
    host_bytes = bytes(int(part) for part in ip_address.split("."))

    port = 8333
    port_bytes = port.to_bytes(2, 'big')

    return services + host_prefix + host_bytes + port_bytes

def send_message(message):
    HOST = "34.146.117.255"
    PORT = 8333

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        s.sendall(message)

        data = s.recv(1024)

        magic, command, payload_length, checksum, payload = parse_header(data)

        print(magic.hex())
        print(command)
        print(payload_length)
        print(checksum.hex())
        print(payload.hex())

    return data

    





def generate_random():
    return os.urandom(8)

def checksum(payload):
   h1 = sha256()
   h1.update(payload)
   firsthex = h1.digest()

   h2=sha256()
   h2.update(firsthex)
   finished_hash = h2.digest()
   checksum = finished_hash[:4]
   return checksum 

  
def parse_header(data):
    magic = data[:4]
    command = data[4:16].rstrip(b"\x00").decode()
    payload_length = int.from_bytes(data[16:20], "little")
    checksum = data[20:24]
    payload = data[24:24 + payload_length]

    return magic, command, payload_length, checksum, payload


def hexprint(byte_array):
    print(binascii.hexlify(byte_array, b" "))
    

# version = 7F 11 01 00 
# services = 01 00 00 00 00 00 00 00 
# timestamp = int(time())
# rec address =  services + inet_addr(ip) + 8333
# sen address = services + inet_addr(ip) + 8333
# node id = 3B 2E B3 5D 8C E6 17 65 
# sub-version string = 0F 2F 53 61 74 6F 73 68 69 3A 30 2E 37 2E 32 2F
# last block = 00
# relay = 00 


version = 70015
version_bytes = version.to_bytes(4, 'little')
hexprint(version_bytes) 

services= bytearray.fromhex("01 00 00 00 00 00 00 00")
hexprint(services)

timestamp = int(time())
timestamp_bytes=timestamp.to_bytes(8, "little")
hexprint(timestamp_bytes)

rec_address = inet_addr(HOST)
hexprint(rec_address)

sen_address = inet_addr("10.0.0.1")
hexprint(sen_address)

node_id = generate_random()
hexprint(node_id)

sub_version_string = "/Satoshi:0.7.2/"  
sub_version_string_length = len(sub_version_string)
sub_version_string_length_bytes = sub_version_string_length.to_bytes(1, 'little')
sub_version_string_bytes = sub_version_string_length_bytes + sub_version_string.encode()
hexprint(sub_version_string_bytes)

last_block = 0 
last_block_bytes = last_block.to_bytes(4, 'little')
hexprint(last_block_bytes)

relay = 0
relay_bytes = relay.to_bytes(1, 'little')
hexprint(relay_bytes)


payload = (
    version_bytes
    + services
    + timestamp_bytes
    + rec_address
    + sen_address
    + node_id
    + sub_version_string_bytes
    + last_block_bytes
    + relay_bytes
)

hexprint(payload)
checksum_bytes=checksum(payload)
hexprint(checksum_bytes)

magic_number = bytearray.fromhex("F9 BE B4 D9")
hexprint(magic_number)

version_command = bytearray.fromhex("76 65 72 73 69 6f 6e 00 00 00 00 00")
hexprint(version_command)

payload_length = len(payload).to_bytes(4, "little")
hexprint(payload_length)

message = (
    magic_number
    + version_command
    + payload_length
    + checksum_bytes
    + payload
)
print ("sending message")
hexprint(message)


response = send_message(message)
print("response from node")
hexprint(response)

payload_length_bytes = response[16:20]
print(payload_length_bytes.hex())  # 66000000

payload_length = int.from_bytes(payload_length_bytes, "little")
print(payload_length)  # 102




first_message_length = 24 + payload_length

second_message = response[first_message_length:]

data = send_message(message)
magic, command, payload_length, checksum, version_payload = parse_header(data)

if command == "version":
    p = version_payload

    version = int.from_bytes(p[0:4], "little")
    services = int.from_bytes(p[4:12], "little")
    timestamp = int.from_bytes(p[12:20], "little")

    addr_recv = p[20:46]
    addr_from = p[46:72]
    nonce = p[72:80]

    user_agent_length = p[80]
    user_agent_start = 81
    user_agent_end = user_agent_start + user_agent_length
    user_agent = p[user_agent_start:user_agent_end].decode()

    start_height = int.from_bytes(p[user_agent_end:user_agent_end + 4], "little")
    relay = p[user_agent_end + 4]

    print("version:", version)
    print("services:", services)
    print("timestamp:", timestamp)
    print("user agent:", user_agent)
    print("start height:", start_height)
    print("relay:", relay)
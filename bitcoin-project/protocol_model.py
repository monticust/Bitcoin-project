from protocolutils import parse_header, parse_version_command, version_command,checksum
from time import time
from socket import inet_aton
from protocolutils import inet_addr
from protocolutils import generate_random

class Message:
    def __init__(
        self,
        magic: bytes,
        command: str,
        payload_length: int,
        checksum: bytes,
        payload: bytes,
    ):
        self.magic = magic
        self.command = command
        self.payload_length = payload_length
        self.checksum = checksum
        self.payload = payload
    
    def to_bytes(self) -> bytes:
        command_bytes = self.command.encode()

        if len(command_bytes) > 12:
            raise ValueError("Bitcoin commands cannot exceed 12 bytes")

        command_bytes += b"\x00" * (12 - len(command_bytes))

        payload_length_bytes = self.payload_length.to_bytes(4, "little")

        return (
           self.magic
           + command_bytes
           + payload_length_bytes
           + self.checksum
           + self.payload
        )

    @classmethod
    def from_command(cls, command: "BaseCommand") -> "Message":
        magic = bytes.fromhex("F9 BE B4 D9")
        if isinstance(command, VersionCommand):
           command_name = "version"

        elif isinstance(command, VerackCommand):
           command_name = "verack"
        
        else:
            raise ValueError("Unsupported command type")
        
        payload = command.to_bytes()
        payload_length = len(payload)
        checksum_bytes = checksum(payload)

        return cls(
            magic,
            command_name,
            payload_length,
            checksum_bytes,
            payload,
        )



    @classmethod
    def from_bytes(cls, data: bytes) -> "Message":
        magic, command, payload_length, checksum, payload = parse_header(data)
        pass

        return cls(
          magic,
          command,
          payload_length,
          checksum,
          payload,
      )
    
    def to_command(self) -> "BaseCommand":
        if self.command == "version":
            (
                version,
                services,
                timestamp,
                addr_recv,
                addr_from,
                nonce,
                user_agent,
                start_height,
                relay,
            ) = parse_version_command(self.payload)

            return VersionCommand(
                version,
                services,
                timestamp,
                addr_recv,
                addr_from,
                nonce,
                user_agent,
                start_height,
                relay,
            )

        elif self.command == "verack":
            return VerackCommand()


class NetAddr:
    def __init__(self, services: int, ip: str, port: int):
        self.services = services
        self.ip = ip
        self.port = port

class BaseCommand:
    def print(self):
        pass
    def to_bytes(self) -> bytes:
        raise NotImplementedError



class VersionCommand(BaseCommand):
    def __init__(
        self,
        version: int,
        services: int,
        timestamp: int,
        addr_recv: bytes,
        addr_from: bytes,
        nonce:bytes,
        user_agent:str,
        start_height: int,
        relay: bool,
    ):
        self.version = version
        self.services = services
        self.timestamp = timestamp
        self.addr_recv = addr_recv
        self.addr_from = addr_from
        self.nonce = nonce
        self.user_agent = user_agent
        self.start_height = start_height
        self.relay = relay
    
    @classmethod
    def from_host(cls, host: str) -> "VersionCommand":
        version = 70015
    
        services = 1

        timestamp = int(time())
    
        addr_recv = inet_addr(host)
        addr_from = inet_addr("10.0.0.1")

        nonce = generate_random()

        user_agent = "/Satoshi:0.7.2/"

        start_height = 0

        relay = 0

        return cls(
        version,
        services,
        timestamp,
        addr_recv,
        addr_from,
        nonce,
        user_agent,
        start_height,
        relay,
      )

    def to_bytes(self) -> bytes:
       version_bytes = self.version.to_bytes(4, "little")
       services_bytes = self.services.to_bytes(8,"little")
       timestamp_bytes = self.timestamp.to_bytes(8, "little")
       last_block_bytes = self.start_height.to_bytes(4,"little")
       relay_bytes = int(self.relay).to_bytes(1,"little")
       user_agent_bytes = self.user_agent.encode()
       user_agent_length = len(user_agent_bytes)
       user_agent_length_bytes = user_agent_length.to_bytes(1,"little")
       
       payload = (
       version_bytes
       + services_bytes
       + timestamp_bytes
       + self.addr_recv
       + self.addr_from
       + self.nonce
       + user_agent_length_bytes
       + user_agent_bytes
       + last_block_bytes
       + relay_bytes
       )

       return payload

    def print(self):
        print("version:", self.version)
        print("services:", self.services)
        print("timestamp:", self.timestamp)
        print("receiver address:", self.addr_recv.hex())
        print("sender address:", self.addr_from.hex())
        print("nonce:", self.nonce.hex())
        print("user agent:", self.user_agent)
        print("start height:", self.start_height)
        print("relay:", self.relay)

class VerackCommand(BaseCommand):
    def print(self):
        print("Handshake acknowledged")
        
from protocolutils import parse_header, parse_version_command

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

    @classmethod
    def from_bytes(cls, data: bytes) -> "Message":
        magic, command, payload_length, checksum, payload = parse_header(data)

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




class VersionCommand(BaseCommand):
    def __init__(
        self,
        version: int,
        services: int,
        timestamp: int,
        addr_recv: bytes,
        addr_from: bytes,
        nonce:bytes,
        user_agent,
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
        
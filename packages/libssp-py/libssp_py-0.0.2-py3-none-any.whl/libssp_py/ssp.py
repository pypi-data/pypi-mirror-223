import socket

from discord import Enum

from libssp_py.util import generate_token


class PacketType(int, Enum):
	INIT = 0x64
	STREAM_METADATA = 0x6e
	STREAM_VIDEO = 0x6f
	STREAM_AUDIO = 0x70
	HANDSHAKE = 0xc8
	STREAM_START = 0xca
        

class SSPClient:
    host: str
    port = 9999
    debug_mode: bool
    socket: socket

    def __init__(self, host: str, debug_mode = False):
        self.host = host
        self.debug_mode = debug_mode
        self.connect()
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self._handshake()
    
    def disconnect(self):
        self.socket.close()
    
    def _debug(self, *args, **kwargs):
        if self.debug_mode:
            # TODO: proper logging
            print(*args, **kwargs)
    
    def _handshake(self):

        # RECEIVE INIT PACKET

        init = self._receive()
        
        assert init[0] == PacketType.INIT.value, "Expected INIT packet, got " + hex(init[0])

        name = init[8:init.index(0, 8)].decode('utf-8')
        
        self._debug(f"<== INIT: device_name={name}")

        challenge = init[43:]
        challenge_response = generate_token(challenge)
        
        # SEND HANDSHAKE

        # TODO: construct the packet more properly
        # handshake = PacketType.HANDSHAKE.value.to_bytes(1) + b'\0\0' + b'zcam-live-user\0' + len(challenge_response).to_bytes(4, byteorder='big') + challenge_response
        handshake = b'\0\0' + b'\x00\x28' + b'\xc8\x00\x00' + b'zcam-live-user\0' + b'\x00\x14' + challenge_response
        assert len(handshake) == 44

        self.socket.send(handshake)
        self._debug("==> HANDSHAKE")

        # RECEIVE HANDSHAKE RESPONSE

        handshake_response = self._receive()
        self._debug("<== HANDSHAKE", handshake_response)

        return True

    def _send(self, data: bytes):
        len_bytes = len(data).to_bytes(4, byteorder='big')
        self.socket.send(len_bytes)
        self.socket.send(data)

    def _receive(self):
        packet_length_field = self.socket.recv(4, socket.MSG_WAITALL)
        packet_length = int.from_bytes(packet_length_field, byteorder='big')
        self._debug("<== PACKET LEN:", packet_length)

        if packet_length > 100000:
            print("Packet length is too large, something is wrong:", packet_length)
            return b''

        data = self.socket.recv(packet_length, socket.MSG_WAITALL)

        return data
    
    def start_streaming(self):
        """Send a request to start streaming."""
        start_request = PacketType.STREAM_START.value.to_bytes(1) + bytes.fromhex('00 00 00 01 00 00 00 00')

        print("==> START_REQUEST", start_request)
        self._send(start_request)

    def stop_streaming(self):
        # TODO: implement stop streaming
        print("TODO: stop streaming is not implemented yet")
    
    def stream_packets(self):
        """And iterator returning raw packets from the stream."""
        self.start_streaming()
        try:
            while True:
                data = self._receive()
                yield data
        except StopIteration:
            self.stop_streaming()

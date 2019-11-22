import asyncio
import logging
import socket


class Ebusd:
    RECONNECT_TO_SEC = 5
    SOCK_TO_SEC = 5

    def __init__(self, loop, address, port=8888):
        self.logger = logging.getLogger(__name__)
        self.loop = loop
        self.address = address
        self.port = port
        self.sock = None

    def __del__(self):
        self.logger.info('Done')

    async def connect(self):
        while True:
            try:
                self.logger.debug('Connecting to ebusd at %s:%d...',
                                  self.address, self.port)
                self.__connect()
                self.logger.info('Connected to ebusd')
            except OSError:
                self.logger.debug('Retrying connection to ebusd')
                await asyncio.sleep(self.RECONNECT_TO_SEC)
            else:
                break

    def __connect(self):
        if self.sock:
            return
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.SOCK_TO_SEC)
            self.sock.connect((self.address, self.port))
        except OSError:
            self.sock = None
            raise

    def __disconnect(self):
        if self.sock:
            self.logger.info('Disconnecting from ebusd')
            self.sock.close()
        self.sock = None

    def __recvall(self):
        # All socket access is serialized with the lock, so we can assume
        # that we can to read all the data in the receive buffer.
        result = b''
        while True:
            # Read as many bytes as we can
            chunk = self.sock.recv(4096)
            if not chunk:
                # Disconnected - reconnect
                self.sock = None
                raise OSError('Disconnected from ebusd')
            result += chunk
            # ebusd response ends with a single empty line.
            if chunk.endswith(b'\n\n'):
                break
        return result

    def __do_io(self, command, retry=3):
        try:
            command += '\n'
            for i in range(retry):
                self.sock.sendall(command.encode())
                result = self.__recvall().decode('utf-8').rstrip()
                # FIXME: sometimes ebusd returns 'Element not found' error
                # even for known messages, so try harder.
                if result != EbusdErr.RESULT_ERR_NOTFOUND.value:
                    break
            # Check if reply is an error message.
            if EbusdErr.has_value(result):
                raise ValueError(result)
        except OSError:
            # Disconnected - reconnect
            self.sock = None
        else:
            raise
        return result


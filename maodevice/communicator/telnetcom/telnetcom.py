# -*- coding: utf-8 -*-
import telnetlib
from ..communicator import Communicator


class TelnetCom(Communicator):
    """Communicate with the device via 'Telnet'.

    This is a child class of the base class 'Communicator'.

    Args:
        host (str): IP Address of a device.
        port (int): Port of a device.
        timeout (int): Set a read timeout values.
            Defaults to 1.

    Attributes:
        method (str): Communication method.
        connection (bool): Connection indicator.
            If it is true, the connection has been established.
        terminator (str): Termination character.
    """
    method = 'Telnet'

    def __init__(self, host: str, port: int, timeout: int=1) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout

    def open(self) -> None:
        """Open the connection to the device.

        Note:
            This method override the 'open' in the base class.

        Return:
            None
        """
        if not self.connection:
            self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
            self.tn.open(self.host, self.port, self.timeout)
            self.connection = True
        return

    def close(self) -> None:
        """Close the connection to the device.

        Note:
            This method override the 'close' in the base class.

        Return:
            None
        """
        self.tn.close()
        del(self.tn)
        self.connection = False
        return

    def send(self, msg: str) -> None:
        """Send a message to the device.

        Note:
            This method override the 'send' in the base class.

        Args:
            msg (str): Message to send the device.

        Return:
            None
        """
        self.tn.write((msg + self.terminator).encode())
        return

    def recv(self, byte: int=1024) -> bytes:
        """Receive the response of the device.

        Note:
            This method override the 'recv' in the base class.

        Args:
            byte (int): Bytes to read. Defaults to 1024.

        Return:
            ret (bytes): The response of the device.
        """
        # ret = self.tn.read_until(byte, self.timeout)
        # return
        pass

    def readlines(self):
        """Receive the multiple rows response of the device.

        Note:
            This method override the 'readlines' in the base class.

        Return:
            ret (:obj:`list` of :obj:`bytes`): The response of the device.
        """
        ret = self.tn.read_until(
            expected=self.terminator.encode(),
            timeout=self.timeout,
        )
        ret = ret.splitlines()
        return ret

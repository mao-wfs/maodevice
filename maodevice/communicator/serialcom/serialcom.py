# -*- coding: utf-8 -*-
import serial
from ..communicator import Communicator
from typing import Union


class SerialCom(Communicator):
    """Communicate with the device via 'Serial'.

    This is a child class of the base class 'Communicator'.

    Args:
        port (str): Device name.
        baudrate (int): Baud rate.
            Defaults to 9600.
        byteize (int): Number of data bits.
            Defaults to serial.EIGHTBITS.
        parity (str): Enable parity checking.
            Defaults to serial.PARITY_NONE.
        stopbits (float): Number of stop bits.
            Defaults to serial.STOPBITS_ONE.
        timeout (float): A read timeout values.
            Defaults to 1.0.
        xonxoff (bool): Enable software flow control.
            Defaults to False.
        rtscts (bool): Enable hardware (RTS/CTS) flow control.
            Defaults to False.
        dsrdtr (bool): Enable hardware (DSR/DTR) flow control.
            Defaults to False.
        write_timeout (float or None): Set a write timeout value.
            Defaults to None.
        inter_byte_timeout (float or None): Inter-character timeout.
            Defaults to None (None to disable).
        exclusive (bool): Set exclusive access mode (POSIX only).
            A port cannot be opened in exclusive access mode
            if it is already open in exclusive access mode.
            Defaults to None.

    Attributes:
        method (str): Communication method.
        connection (bool): Connection indicator.
            If it is true, the connection has been established.
        terminator (str): Termination character.
    """
    method = 'Serial'

    def __init__(
            self,
            port: str,
            baudrate: int=9600,
            bytesize: int=serial.EIGHTBITS,
            parity: str=serial.PARITY_NONE,
            stopbits: float=serial.STOPBITS_ONE,
            timeout: float=1.,
            xonxoff: bool=False,
            rtscts: bool=False,
            dsrdtr: bool=False,
            write_timeout: Union[float, None]=None,
            inter_byte_timeout: Union[float, None]=None,
            exclusive: bool=None,
    ) -> None:
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.dsrdtr = dsrdtr
        self.write_timeout = write_timeout
        self.inter_byte_timeout = inter_byte_timeout
        self.exclusive = exclusive

    def open(self) -> None:
        """Open the connection to the device.

        Note:
            This method override the 'open' in the base class.

        Return:
            None
        """
        if not self.connection:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                timeout=self.timeout,
                xonxoff=self.xonxoff,
                rtscts=self.rtscts,
                dsrdtr=self.dsrdtr,
                write_timeout=self.write_timeout,
                inter_byte_timeout=self.inter_byte_timeout,
                exclusive=self.exclusive,
            )
            self.connection = True
        return

    def close(self) -> None:
        """Close the connection to the device.

        Note:
            This method override the 'close' in the base class.

        Return:
            None
        """
        self.ser.close()
        del(self.ser)
        self.connection = False
        return

    def send(self, msg: str) -> None:
        """Send a message to the device.

        Note:
            This method override the 'send' in the base class.

        Args:
            msg (str): A Message to send the device.

        Return:
            None
        """
        self.ser.write((msg + self.terminator).encode())
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
        ret = self.ser.read(size=byte)
        return ret

    def readlines(self):
        """Receive the multiple rows response of the device.

        Note:
            This method override the 'readlines' in the base class.

        Return:
            ret (:obj:`list` of :obj:`bytes`): The response of the device.
        """
        ret = self.ser.readlines()
        return ret

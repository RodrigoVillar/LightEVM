"""
Module containing the transaction/message classes for the EVM
"""
from utils.u256 import *
from utils.address import EVMAddress

class EVMTransaction():
    """
    Values should be immutable
    """

    def __init__(self, tx_type: int, gas_price: int, gas_limit: int, origin: EVMAddress):

        self._tx_type = None
        self._nonce = None
        self._gas_price = None
        self._gas_limit = None
        # MUST BE EOA
        self._origin = None

    def get_tx_type(self):

        return self._tx_type

    def get_nonce(self):

        return self._nonce

    def get_gas_price(self):

        return self._gas_price

    def get_gas_limit(self):

        return self._gas_limit
    
    def get_origin(self):

        return self._origin

class EVMMessage():
    """
    Values can mutate between internal transactions
    """
    def __init__(self, data: str, sig: str, value: int, recipient: EVMAddress):

        # Data passed with message (HEX)
        self._data = None
        # Sender of message
        self._sender = None
        # Function selector
        self._sig = None
        # Denominated in Wei
        self._value = None
        # Contract whose code will be executed
        self._recipient = None
        
    def get_data(self):
        """
        Returns message data in its entirety
        """
        return self._data

    def get_sender(self):

        return self._sender

    def get_sig(self):

        return self._sig

    def get_value(self):

        return self._value

    def get_recipient(self):

        return self._recipient

    def load_data(self, i: U256) -> U256:
        """
        Returns the equivalent of msg.data[i:i+32]

        If i + 32 is greater than the rightmost index, return value is
        right-padded with 0s
        """
        data_list = list(self._data)
        data_str = ""
        for i in range(i * 2, (i * 2) + 64):

            try:
                data_str += data_list[i]
            except:
                data_str += "00"

        data_int = int(data_str, 16)
        return U256(data_int)

    def get_data_size(self) -> U256:
        """
        Returns size of message data in bytes
        """
        pass

    def load_data_custom(self, offset: U256, length: U256) -> str:

        pass

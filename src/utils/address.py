"""
Module containing the address type
"""

from .u256 import *

class EVMAddressFailedInitialization(Exception):

    pass

class EVMAddress():

    def __init__(self, uint: U256 = None, hex: str = None):

        self._hex_representation = None
        self._uint_representation = None


        if uint != None:
            self._uint_representation = uint
            self._hex_representation = U256.to_address_hex(int)
        elif hex != None:
            self._hex_representation == EVMAddress.format(hex)
            self._uint_representation == U256.from_hex(EVMAddress.format(hex))
        else:
            raise EVMAddressFailedInitialization()      

    def get_uint(self) -> U256:

        return self._uint_representation

    def get_hex(self) -> str:

        return self._hex_representation

    def get_hex_with_prefix(self) -> str:

        return "0x" + self._hex_representation

    @staticmethod
    def format(address: str) -> str:
        # First remove prefix if possible
        if address[:2].lower() == "0x":
            address = address[2:]

        address = address.lower()

        # Check length
        hex_str_len = len(address)
        # How many zeros to prepend if necessary
        preprend_len = 40 - hex_str_len
        for i in range(preprend_len):
            address = "0" + address

        return address
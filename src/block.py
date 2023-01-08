"""
Module containing the Block class
"""
from utils.address import EVMAddress
from utils.u256 import U256

class EVMBlock():

    def __init__(self, base_fee: int, number: int, gas_limit: int, coinbase: EVMAddress, timestamp: int, difficulty: int):

        self._base_fee = base_fee
        self._number = number
        self._gas_limit = gas_limit
        self._coinbase = coinbase
        self._timestamp = timestamp
        self._difficulty = difficulty

    def get_base_fee(self) -> U256:

        return U256(self._base_fee)

    def get_number(self) -> U256:

        return U256(self._number)

    def get_gas_limit(self) -> U256:

        return U256(self._gas_limit)

    def get_coinbase(self) -> EVMAddress:

        return self._coinbase

    def get_timestamp(self) -> U256:

        return U256(self._timestamp)

    def get_difficulty(self) -> U256:

        return U256(self._difficulty)


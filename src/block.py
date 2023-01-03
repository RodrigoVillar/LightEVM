"""
Module containing the Block class
"""

class EVMBlock():

    def __init__(self):

        self._base_fee = None
        self._number = None
        self._gas_limit = None
        self._coinbase = None
        self._timestamp = None
        self._difficulty = None

    def get_base_fee(self):

        return self._base_fee

    def get_number(self):

        return self._number

    def get_gas_limit(self):

        return self._gas_limit

    def get_coinbase(self):

        return self._coinbase

    def get_timestamp(self):

        return self._timestamp

    def get_difficulty(self):

        return self._difficulty


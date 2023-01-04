"""
Module containg the state class and the storage component of the EVM
"""
from utils.u256 import *

class EVMTouchedAddresses():
    """
    Addresses are lowercase hexadecimal strings

    Since touched addresses persist between messages, a remove() method does not
    need to be implemented
    """

    def __init__(self):

        self._set = set()

    def add(self, address: str):

        address = address.lower()

        if address not in self:

            self._set.add(address)


class EVMTouchedSlots():

    def __init__(self):
    
        # Maps EVMAddress values to int sets
        self._mapping = {}

    def add_slot(self, address: str, key: U256):

        address = address.lower()

        if address not in self._mapping:
            self._mapping[address] = set()
            self._mapping[address].add(key.to_int())

        self._mapping[address].add(key.to_int())

    def contains_address(self, address: str):

        address = address.lower()

        if address in self._mapping:

            return True

        return False

    def is_slot_touched(self, address: str, key: U256):

        address = address.lower()

        slot_int = key.to_int()

        if slot_int in self._mapping[address]:
            
            return True

        return False

class EVMAccessSet():

    def __init__(self):

        self._touched_addresses = EVMTouchedAddresses()
        self._touched_slots = EVMTouchedSlots()

    def add_touched_address(self, address: str):

        self._touched_addresses.add(address)

    def add_slot(self, address: str, key: U256):

        self._touched_slots.add_slot(address, key)

    def is_slot_touched(self, address: str, key: U256):

        self._touched_slots.is_slot_touched(address, key)

class EVMStorageMap():

    def __init__(self):

        self._map = {}

    def load(self, address: str, key: U256):

        pass

    def store(self, address: str, key: U256):

        pass   

    def load_ext(self, address: str, key: U256):
        """
        Grab contract storage from internet
        """
        pass

    def contains_address(self, address: str) -> bool:

        address = address.lower()

        if address not in self._map:

            return False

        return True

    

class EVMStorage():
    """
    Class representing storage
    """
    def __init__(self):

        self._storage = EVMStorageMap()
        self._access_set = EVMAccessSet()

    def get(self, address: str, key: U256) -> U256:

        if key.to_int() not in self._storage:

            return U256(0)

        return self._storage[key.to_int()]

    def store(self, key: U256, value: U256):

        pass

    def touch_address(self, address: str):

        self._access_set.add_touched_address(address)

class EVMGlobalState():
    """
    Class holding information regarding the blockchain
    """

    def __init__(self, chain_id = None):

        self._chain_id = chain_id
        self._access_set = EVMAccessSet()

    def get_account_balance(self, address: U256) -> U256:

        pass

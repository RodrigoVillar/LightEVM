"""
Module containg the state class and the storage component of the EVM
"""
from .utils.u256 import U256
from .utils.address import EVMAddress
from dotenv import dotenv_values    
from web3 import Web3
import os

class EVMGlobalState():
    """
    Class holding information regarding the blockchain
    """

    def __init__(self, chain_id: int = None):

        self._chain_id = chain_id

    def get_chain_id(self) -> int:

        return self._chain_id

class EVMContractStorage():

        def __init__(self, bytecode: str, slots: dict):
            """
            Slots maps ints to U256 values
            """
            bytecode = bytecode.lower() 
            if bytecode[:2] == "0x":

                bytecode = bytecode[2:]

            self._bytecode: str = bytecode
            self._slots: dict[int: U256] = slots
            # Copy of original self._slots, immutable
            self._immutable_slots: dict[int, U256] = slots.copy()

        def add_modified_slot(self, frame_number: int, slot: U256):

            if frame_number not in self._modified_slots:

                self._modified_slots[frame_number] = set()

            self._modified_slots[frame_number].add(slot.to_int())

        def reset_modified_slots(self, frame_number: int):
            """
            To be called at the end of every EVM execution context
            """
            if frame_number not in self._modified_slots:

                return

            self._modified_slots[frame_number].clear()

        def get_bytecode(self) -> str:

            return self._bytecode

        def get_bytecode_size(self) -> U256:

            size = len(self._bytecode) // 2

            return U256(size)

        def get_slot_value(self, key: int) -> U256:

            if key not in self._slots:

                return U256(0)

            return self._slots[key]

        def get_imumutable_slot_value(self, key: int) -> U256:

            if key not in self._immutable_slots:

                return U256(0)

            return self._immutable_slots[key]

        def set_slot_value(self, key: int, value: U256):

            self._slots[key] = value

        def get_bytecode_custom(self, offset: U256, length: U256) -> str:

            offset_val = offset.to_int()
            length_val = length.to_int()

            result = ""

            for i in range(length_val):

                result = result + self._bytecode[offset_val + (i * 2): offset_val + (i * 2) + 2]

            return result

class EVMStorageMap():

    def __init__(self, block_number: int):

        # Maps contract addresses to contract storage objects
        self._contract_mapping: dict[str: EVMContractStorage] = {}
        # Maps contract address to U256 values representing balances
        self._balance_mapping: dict[str: U256] = {}

        url = os.getenv("API_URL")
        self._w3 = Web3(Web3.HTTPProvider(url))

        self._block_number = block_number

    def grab_contract(self, address: EVMAddress):
        """
        Function that is called whenever the EVM requests data from a smart
        contract, but said contract has no data stored locally. Using the
        provided RPC URL, grab_contract() pulls all data necessary to store the
        contract locally

        Ref: https://medium.com/coinmonks/a-practical-walkthrough-smart-contract-storage-d3383360ea1b
        """
        bytecode = str(self._w3.eth.get_code(address.get_hex_with_prefix(), self._block_number))[2:]
        balance = int(self._w3.eth.get_balance(address.get_hex_with_prefix(), self._block_number))

        # Maps keys to values, int to U256
        slot_map: dict[int: U256] = {}

        zero_counter = 0
        slot_counter = 0
        while zero_counter < 0:

            slot_value = int(str(self._w3.eth.get_storage_at(address.get_hex_with_prefix(), slot_counter, self._block_number)), 16)

            if slot_value != 0:
                slot_map[slot_counter] = U256(slot_value)

            slot_counter += 1
            zero_counter += 1

        contract_storage = EVMContractStorage(bytecode, slot_map)
        self.add_contract(address, contract_storage, U256(balance))

    def add_contract(self, address: EVMAddress, data: EVMContractStorage, balance: U256):

        self._contract_mapping[address.get_hex()] = data
        self._balance_mapping[address.get_hex()] = balance

    def set_slot_value(self, address: EVMAddress, slot_key: U256, slot_value: U256):

        if address.get_hex() not in self._contract_mapping:

            self.grab_contract(address)

        self._contract_mapping[address.get_hex()].set_slot_value(slot_key.to_int(), slot_value)

    def get_slot_value(self, address: EVMAddress, slot_key: U256) -> U256:

        if address.get_hex() not in self._contract_mapping:

            self.grab_contract(address)

        return self._contract_mapping[address.get_hex()].get_slot_value(slot_key.to_int())

    def get_immutable_slot_value(self, address: EVMAddress, slot_key: U256) -> U256:

        if address.get_hex() not in self._contract_mapping:

            self.grab_contract(address)

        return self._contract_mapping[address.get_hex()].get_imumutable_slot_value(slot_key.to_int())

    def get_contract_bytecode(self, address: EVMAddress) -> str:

        if address.get_hex() not in self._contract_mapping:

            self.grab_contract(address)

        return self._contract_mapping[address.get_hex()].get_bytecode()

    def get_contract_balance(self, address: EVMAddress):

        if address.get_hex() not in self._balance_mapping:

            self.grab_contract(address)
        
        return self._balance_mapping[address.get_hex()]

    def get_contract_bytecode_size(self, address: EVMAddress) -> U256:

        if address.get_hex() not in self._balance_mapping:

            self.grab_contract(address)
        
        return self._contract_mapping[address.get_hex()].get_bytecode_size()

    def get_contract_bytecode_custom(self, address: EVMAddress, offset: U256, length: U256) -> str:

        if address.get_hex() not in self._balance_mapping:

            self.grab_contract(address)
        
        return self._contract_mapping[address.get_hex()].get_bytecode_custom(offset, length)

    def is_slot_modified(self, address: EVMAddress, frame_number: int, slot: U256):

        if address.get_hex() not in self._contract_mapping:

            self.grab_contract(address)

        return self._contract_mapping[address.get_hex()].is_slot_modified()

class EVMAccessMap():
    """
    Class that incorporates the accessed addresses and the accessed storage
    slots management of EIP-2929
    """

    def __init__(self) -> None:
        # Set of addresses, all lowercase strings
        self._touched_addresses = set()
        # Dictionary that maps lowercase strings representing addressses to sets
        # which contains ints that represent storage keys
        self._touched_storage_slots = {}

    def add_touched_address(self, address: EVMAddress):

        self._touched_addresses.add(address.get_hex())

    def add_touched_storage_slot(self, address: EVMAddress, key: U256):

        if address.get_hex() not in self._touched_storage_slots:

            self._touched_storage_slots[address.get_hex()] = set()

        self._touched_storage_slots[address.get_hex()].add(key.to_int())

    def is_address_touched(self, address: EVMAddress) -> bool:

        return address.get_hex() in self._touched_addresses

    def is_storage_slot_touched(self, address: EVMAddress, key: U256) -> bool:

        try:
            return key.to_int() in self._touched_storage_slots[address.get_hex()]
        except KeyError: # Address not found
            return False


class EVMStorage():
    """
    Class responsible for maintaining the EVM storage component with is divided
    up via the EVMStorageMap classes and the EVMAccessMap classes

    EVMStorage is first initialized via the parameters passed in the
    execution.toml file. Anytime an instance of the EVM requires access to
    storage, EVMStorage will first check if the data in question is stored
    locally. If not, EVMStorage will retrieve said data (and all other data of
    the associated contract address) and will store it locally for the rest of
    the execution runtime.
    """

    def __init__(self, block_number):

        self._access_map = EVMAccessMap()
        self._storage_map = EVMStorageMap(block_number)

    def load(self, address: EVMAddress, slot: U256) -> U256:

        is_touched = self._access_map.is_storage_slot_touched(address, slot)

        if not is_touched:

            self._access_map.add_touched_storage_slot(address, slot)
        
        return self._storage_map.get_slot_value(address, slot)

    def store(self, address: EVMAddress, slot: U256, slot_value: U256):
        # NEED TO EVENTUALLY IMPLEMENT GAS REFUNDS
        is_touched = self._access_map.is_storage_slot_touched(address, slot)

        if not is_touched:

            self._access_map.add_touched_storage_slot(address, slot)

        # Also need to add contract to touched addresses if not already 
        is_address_touched = self._access_map.is_address_touched(address)

        if not is_address_touched:

            self._access_map.add_touched_address(address)

        self._storage_map.set_slot_value(address, slot, slot_value)
    
    def is_address_touched(self, address: EVMAddress) -> bool:

        return self._access_map.is_address_touched(address)

    def is_storage_slot_touched(self, address: EVMAddress, slot_key: U256) -> bool:

        return self._access_map.is_storage_slot_touched()

    def get_contract_bytecode(self, address: EVMAddress) -> str:

        is_touched = self._access_map.is_address_touched(address)

        if not is_touched:

            self._access_map.add_touched_address(address)

        return self._storage_map.get_contract_bytecode(address)

    def add_touched_address(self, address: EVMAddress):
        """
        Front facing function to add touched addresses
        """
        self._access_map.add_touched_address(address)

    def add_touched_storage_slot(self, address: EVMAddress, key: U256):

        self._access_map.add_touched_storage_slot(address, key)

    def add_contract(self, address: EVMAddress, data: EVMContractStorage, balance: U256):

        self._storage_map.add_contract(address, data, balance)

    def get_contract_bytecode_size(self, address: EVMAddress) -> U256:

        is_touched = self._access_map.is_address_touched(address)

        if not is_touched:

            self._access_map.add_touched_address(address)

        return self._storage_map.get_contract_bytecode_size(address)

    def get_contract_bytecode_custom(self, address: EVMAddress, offset: U256, length: U256):

        is_touched = self._access_map.is_address_touched(address)

        if not is_touched:

            self._access_map.add_touched_address(address)

        return self._storage_map.get_contract_bytecode_custom(address, offset, length)

    def get_contract_balance(self, address: EVMAddress):

        is_touched = self._access_map.is_address_touched(address)

        if not is_touched:

            self._access_map.add_touched_address(address)

        return self._storage_map.get_contract_balance()

    def load_immutable(self, address: EVMAddress, key: U256):

        return self._storage_map.get_immutable_slot_value(address, key)
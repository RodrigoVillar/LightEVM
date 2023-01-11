"""
Module containing the EVM Input class
"""

from state import EVMStorage, EVMContractStorage
from utils.address import EVMAddress
from utils.u256 import U256
from logs import EVMLogStorage

class EVMInput():

    def __init__(self):

        self._storage = None

    def from_toml(self, toml_dict: dict):

        # Chain properties
        self._chain_id = toml_dict["chain"]["chain_id"]
        # Block properties
        self._timestamp = toml_dict["block"]["timestamp"]
        self._difficulty = toml_dict["block"]["difficulty"]
        self._block_gas_limit = toml_dict["block"]["gas_limit"]
        self._base_fee = toml_dict["block"]["base_fee"]
        self._block_number = toml_dict["block"]["number"]
        self._coinbase = toml_dict["block"]["coinbase"]

        # Transaction properties
        self._from: EVMAddress = EVMAddress(hex = toml_dict["transaction"]["from"])
        self._to: EVMAddress = EVMAddress(hex = toml_dict["transaction"]["to"])
        self._calldata = toml_dict["transaction"]["calldata"]
        self._value = toml_dict["transaction"]["value"]
        self._tx_gas_limit = toml_dict["transaction"]["gas_limit"]
        self._gas_price = toml_dict["transaction"]["gas_price"]
        self._type = toml_dict["transaction"]["type"]
        self._signature = toml_dict["transaction"]["sig"]

        self._storage = EVMStorage(self._block_number)
        self._log_storage = EVMLogStorage()

        if "contracts" in toml_dict:

            for contract in toml_dict["contracts"]:

                formatted_slots = {}

                for slot_key in contract["slots"]:

                    formatted_slots[int(slot_key)] = contract["slots"][slot_key]

                contract_storage = EVMContractStorage(contract["bytecode"], formatted_slots)
                self._storage.add_contract(EVMAddress(hex=contract["address"]), contract_storage, U256(contract["balance"]))

        self._frame_number = 0

    def get_log_storage(self) -> EVMLogStorage:

        return self._log_storage

    def set_log_storage(self, log_storage: EVMLogStorage):

        self._log_storage = log_storage

    def get_frame_number(self) -> int:

        return self._frame_number

    def set_frame_number(self, frame_number: int):

        self._frame_number = frame_number

    def set_chain_id(self, id):

        self._chain_id = id

    def set_timestamp(self, timestamp):

        self._timestamp = timestamp

    def set_difficulty(self, difficulty):

        self._difficulty = difficulty

    def set_block_gas_limit(self, gas_limit):

        self._block_gas_limit = gas_limit

    def set_base_fee(self, base_fee):

        self._base_fee = base_fee

    def set_from(self, from_addr: EVMAddress):

        self._from = from_addr

    def set_to(self, to: EVMAddress):

        self._to = to

    def set_calldata(self, calldata):

        self._calldata = calldata

    def set_value(self, value):

        self._value = value

    def set_tx_gas_limit(self, limit):

        self._tx_gas_limit = limit

    def set_gas_price(self, price):

        self._gas_price = price

    def set_storage(self, storage: EVMStorage):

        self._storage = storage

    def get_chain_id(self):

        return self._chain_id

    def get_timestamp(self):

        return self._timestamp

    def get_difficulty(self):

        return self._difficulty

    def get_block_gas_limit(self):

        return self._block_gas_limit

    def get_base_fee(self):

        return self._base_fee

    def get_from(self) -> EVMAddress:

        return self._from

    def get_to(self) -> EVMAddress:

        return self._to

    def get_calldata(self):

        return self._calldata

    def get_value(self):

        return self._value

    def get_tx_gas_limit(self):

        return self._tx_gas_limit

    def get_gas_price(self):

        return self._gas_price

    def get_storage(self):

        return self._storage

    def set_block_number(self, number):

        self._block_number = number
    
    def get_block_number(self):

        return self._block_number

    def get_tx_type(self):

        return self._type

    def set_tx_type(self, type: int):

        self._type = type

    def get_signature(self):

        return self._signature

    def set_signature(self, signature: str):

        self._signature = signature

    def get_coinbase(self) -> EVMAddress:

        return self._coinbase

    def set_coinbase(self, coinbase: EVMAddress):

        self._coinbase = coinbase

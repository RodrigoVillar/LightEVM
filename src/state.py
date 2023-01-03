"""
Module containg the state class
"""
from utils.u256 import *

class EVMGlobalState():

    def __init__(self):

        self._chain_id = None

    def get_account_balance(self, address: U256) -> U256:

        pass

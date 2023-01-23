"""
Module containg logic for hashing

keccak256() can be found here
"""

from web3 import Web3

def keccak256(hex: str):

    # Execute hexadecimal logic
    hashed_value = Web3.keccak(hexstr=hex).hex()

    return hashed_value[2:]


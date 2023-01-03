"""
Module containg logic for hashing

keccak256() can be found here
"""

from web3 import Web3

class InvalidKeccakKeyword(Exception):

    pass

def keccak256(**kwargs):

    if "hex" in kwargs:
        # Execute hexadecimal logic
        hex_as_int = int(kwargs["hex"], 16)
        hashed_value = Web3.keccak(hex_as_int).hex()
    elif "binary" in kwargs:
        # Execute binary logic
        pass
    elif "decimal" in kwargs:
        # Execute decimal logic
        pass
    else:
        # User passed in invalid keyword
        raise InvalidKeccakKeyword(kwargs)


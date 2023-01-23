from src.utils.hashing import keccak256
import pytest

class TestKeccak:

    class TestHex:

        def test_one(self):

            value = "00000000"
            return_val = keccak256(hex=value)
            assert(return_val == "e8e77626586f73b955364c7b4bbf0bb7f7685ebd40e852b164633a4acbd3244c")

        def test_two(self): 

            value = "FFFFFFFF"
            return_val = keccak256(hex = value)
            assert(return_val == "29045a592007d0c246ef02c2223570da9522d0cf0f73282c79a1bc8f0bb2c238")

        def test_three(self):

            value = "0000000000000000000000000000000000000000000000000000000000000000"
            return_val = keccak256(hex = value)
            assert(return_val == "290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563")

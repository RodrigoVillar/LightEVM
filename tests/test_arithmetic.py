from src.utils.u256 import U256
from src.utils.exceptions import *
import pytest

class TestUintInitialization:

    def test_one(self):

        uint = U256(1)
        assert(1 == uint.to_int())

    def test_two(self):

        with pytest.raises(U256InvalidInputType):

            U256("str")

    def test_three(self):

        with pytest.raises(U256InputOutOfBounds):

            U256(-1)

    def test_four(self):

        with pytest.raises(U256InputOutOfBounds):

            U256(2**256)

    def test_five(self):

        uint = U256(2**256 - 1)
        assert((2**256 - 1) == uint.to_int())

class TestUintMethods():

    pass
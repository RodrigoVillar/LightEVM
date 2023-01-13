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

    class TestUintBinary:

        def test_one(self):

            x = U256(1)

            assert(
                x.to_binary_string() == "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
            )

        def test_two(self):

            x = U256(2 ** 256 - 1)

            assert(
                x.to_binary_string() == "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
                )

    class TestUintHex:

        def test_one(self):

            x = U256(1)

            assert(
                x.to_hex_string() == "0000000000000000000000000000000000000000000000000000000000000001")

        def test_two(self):

            x = U256(2**256 - 1)

            assert(x.to_hex_string() == "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")

        def test_three(self):

            x = U256(2**256 - 1)

            assert(str(x) == "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")

        def test_four(self):

            x = U256(1)

            assert(x.to_address_hex() == "0000000000000000000000000000000000000001")

        def test_five(self):

            x = U256(2**160 - 1)

            assert(x.to_address_hex() == "ffffffffffffffffffffffffffffffffffffffff")

            x = U256(1015095423264477684803135833436231739418760611879)

            assert(x.to_address_hex() == "b1ce73fafb7d508f26cb8ddf1b817a79239e8827")

        def test_six(self):

            x = U256.from_hex("b1ce73fafb7d508f26cb8ddf1b817a79239e8827")

            assert(x.to_int() == 1015095423264477684803135833436231739418760611879 )

        def test_seven(self):

            x = U256.from_hex("0xb1ce73fafb7d508f26cb8ddf1b817a79239e8827")

            assert(x.to_int() == 1015095423264477684803135833436231739418760611879 )

    class TestUintSigned():

        def test_one(self):

            x = U256.from_signed_integer(-1)

            assert(x.to_binary_string() == "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")

        def test_two(self):

            x = U256(57896044618658097711785492504343953926634992332820282019728792003956564819968)

            assert(x.to_signed_int() == -2**255)

        def test_three(self):

            x = U256.from_signed_integer(-1)

            assert(x.to_signed_int() == -1)

        def test_three(self):

            with pytest.raises(U256InputOutOfBounds):

                x = U256.from_signed_integer(-(2**255) - 1)

        def test_four(self):

            with pytest.raises(U256InputOutOfBounds):

                x = U256.from_signed_integer(2**255)
    
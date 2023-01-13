import pytest
from src.utils.u256 import U256

class TestLT:

    def test_one(self):

        a = U256(1)
        b = U256(2)

        c = U256.lt(a, b)
        assert(c.to_int() == 1)

    def test_two(self):

        a = U256(11)
        b = U256(10)

        c = U256.lt(a, b)
        assert(c.to_int() == 0)

    def test_three(self):

        a = U256(15)
        b = U256(15)

        c = U256.lt(a, b)
        assert(c.to_int() == 0)

class TestGT:

    def test_one(self):

        a = U256(2)
        b = U256(1)
        
        c = U256.gt(a, b)
        assert(c.to_int() == 1)

    def test_two(self):

        a = U256(10)
        b = U256(11)

        c = U256.gt(a, b)
        assert(c.to_int() == 0)

    def test_three(self):

        a = U256(10)
        b = U256(10)

        c = U256.gt(a, b)
        assert(c.to_int() == 0)

class TestSLT:

    def test_one(self):

        a = U256.from_signed_integer(-1)
        b = U256.from_signed_integer(0)

        c = U256.slt(a, b)
        assert(c.to_int() == 1)

    def test_two(self):

        a = U256.from_signed_integer(-2)
        b = U256.from_signed_integer(-1)

        c = U256.slt(a, b)
        assert(c.to_int() == 1)

    def test_three(self):

        a = U256.from_signed_integer(-1)
        b = U256.from_signed_integer(-1)

        c = U256.slt(a, b)
        assert(c.to_int() == 0)

    def test_four(self):

        a = U256.from_signed_integer(2)
        b = U256.from_signed_integer(-5)

        c = U256.slt(a, b)
        assert(c.to_int() == 0)

    def test_five(self):

        a = U256.from_signed_integer(-19)
        b = U256.from_signed_integer(88)

        c = U256.slt(a, b)
        assert(c.to_int() == 1)

    def test_six(self):

        a = U256.from_signed_integer(55)
        b = U256.from_signed_integer(75)

        c = U256.slt(a, b)
        assert(c.to_int() == 1)

class TestSGT:

    def test_one(self):

        a = U256.from_signed_integer(-2)
        b = U256.from_signed_integer(-3)

        c = U256.sgt(a, b)
        assert(c.to_int() == 1)

    def test_two(self):

        a = U256.from_signed_integer(-19)
        b = U256.from_signed_integer(-23)

        c = U256.sgt(a, b)
        assert(c.to_int() == 1)

    def test_three(self):

        a = U256.from_signed_integer(-3)
        b = U256.from_signed_integer(-3)

        c = U256.sgt(a, b)
        assert(c.to_int() == 0)

    def test_four(self):

        a = U256.from_signed_integer(49)
        b = U256.from_signed_integer(19)

        c = U256.sgt(a, b)
        assert(c.to_int() == 1)

    def test_five(self):

        a = U256.from_signed_integer(476)
        b = U256.from_signed_integer(500)

        c = U256.sgt(a, b)
        assert(c.to_int() == 0)

    def test_six(self):
        
        a = U256.from_signed_integer(-823)
        b = U256.from_signed_integer(499)

        c= U256.sgt(a, b)
        assert(c.to_int() == 0)

    def test_seven(self):

        a = U256.from_signed_integer(10089)
        b = U256.from_signed_integer(-3)

        c = U256.sgt(a, b)
        assert(c.to_int() == 1)

class TestEQ:

    def test_one(self):

        a = U256(1)
        b = U256(1)

        c = U256.eq(a, b)
        assert(c.to_int() == 1)

    def test_two(self):

        a = U256(0)
        b = U256(0)

        c = U256.eq(a, b)
        assert(c.to_int() == 1)

    def test_three(self):

        a = U256(19)
        b = U256(21)

        c = U256.eq(a, b)
        assert(c.to_int() == 0)

    def test_four(self):

        a = U256(30)
        b = U256(20)

        c = U256.eq(a, b)
        assert(c.to_int() == 0)

class TestIsZero:

    def test_one(self):

        a = U256(0)
        
        b = U256.is_zero(a)
        assert(b.to_int() == 1)

    def test_two(self):

        a = U256(11)

        b = U256.is_zero(a)
        assert(b.to_int() == 0)

class TestAND:

    def test_one(self):

        a = U256(1)
        b = U256(0)

        c = U256.bitwise_and(a, b)
        assert(c.to_int() == 0)

    def test_two(self):

        a = U256(1)
        b = U256(1)
        
        c = U256.bitwise_and(a, b)
        assert(c.to_int() == 1)

    def test_three(self):

        a = U256(2**256 - 1)
        b = U256(1)

        c = U256.bitwise_and(a, b)
        assert(c.to_int() == 1)

    def test_four(self):

        a = U256(2**256 - 1)
        b = U256(2**256 - 1)

        c = U256.bitwise_and(a, b)
        assert(c.to_int() == 2**256 - 1)

class TestOR:

    def test_one(self):

        a = U256(0)
        b = U256(0)

        c = U256.bitwise_or(a, b)
        assert(c.to_int() == 0)

    def test_two(self):

        a = U256(115792089237316195423570985008687907852929702298719625575994209400481361428480)
        b = U256(340282366920938463463374607431768211455)

        c = U256.bitwise_or(a, b)
        assert(c.to_int() == 2**256 - 1)

    def test_three(self):

        a = U256(2)
        b = U256(1)

        c = U256.bitwise_or(a, b)
        assert(c.to_int() == 3)

class TestXOR:

    def test_one(self):

        a = U256(1)
        b = U256(0)

        c = U256.bitwise_xor(a, b)
        assert(c.to_int() == 1)

    def test_two(self):

        a = U256(1)
        b = U256(1)

        c = U256.bitwise_xor(a, b)
        assert(c.to_int() == 0)

    def test_three(self):

        a = U256(0)
        b = U256(0)

        c = c = U256.bitwise_xor(a, b)
        assert(c.to_int() == 0)

class TestNOT:

    def test_one(self):

        a = U256(2**256 - 1)

        b = U256.bitwise_not(a)
        assert(b.to_int() == 0)

    def test_two(self):

        a = U256(0)

        b = U256.bitwise_not(a)
        assert(b.to_int() == 2**256 - 1)


class TestByte:

    def test_one(self):

        i = U256(31)
        x = U256(256)

        b = U256.byte(i, x)
        assert(b.to_int() == 0)

    def test_two(self):

        i = U256(32)
        x = U256(1)

        b = U256.byte(i, x)
        assert(b.to_int() == 0)

    def test_three(self):

        i = U256(31)
        x = U256(256+255)

        b = U256.byte(i, x)
        assert(b.to_int() == 255)

class TestSHL:

    def test_one(self):

        shift = U256(1)
        value = U256(16)

        b = U256.shl(shift, value)
        assert(b.to_int() == 32)

    def test_two(self):

        shift = U256(10)
        value = U256(0)

        b = U256.shl(shift, value)
        assert(b.to_int() == 0)

    def test_three(self):

        shift = U256(1)
        value = U256(2**255)

        b = U256.shl(shift, value)
        assert(b.to_int() == 0)

class TestSHR:

    def test_one(self):

        shift = U256(2)
        value = U256(32)

        b = U256.shr(shift, value)
        assert(b.to_int() == 8)

    def test_two(self):

        shift = U256(4)
        value = U256(0)

        b = U256.shr(shift, value)
        assert(b.to_int() == 0)

    def test_three(self):

        shift = U256(1)
        value = U256(340282366920938463463374607431768211454)

        b = U256.shr(shift, value)
        assert(b.to_int() == 170141183460469231731687303715884105727)

class TestSAR:

    def test_one(self):

        shift = U256(1)
        value = U256(115792089237316195423570985008687907853269984665640564039457584007913129639934)

        b = U256.sar(shift, value)
        assert(b.to_int() == 2**256 - 1)

    def test_two(self):

        shift = U256(1)
        value = U256(2)

        b = U256.sar(shift, value)
        assert(b.to_int() == 1)
from src.utils.u256 import U256

class TestAdd:

    def test_one(self):

        a = U256(1)
        b = U256(1)

        c = U256.add(a, b)

        assert(c.to_int() == 2)

    def test_two(self):

        a = U256(2**256 - 1)
        b = U256(1)

        c = U256.add(a, b)
        assert(c.to_int() == 0)

class TestMul:

    def test_one(self):

        a = U256(3)
        b = U256(4)

        c = U256.mul(a, b)
        assert(c.to_int() == 12)

    def test_two(self):

        a = U256(2**255)
        b = U256(2)

        c = U256.mul(a, b)
        assert(c.to_int() == 0)

class TestSub:

    def test_one(self):

        a = U256(2)
        b = U256(1)

        c = U256.sub(a, b)
        assert(c.to_int() == 1)

    def test_two(self):

        a = U256(0)
        b = U256(1)

        c = U256.sub(a, b)
        assert(c.to_int() == (2**256 - 1))

class TestDiv:

    def test_one(self):

        a = U256(5)
        b = U256(2)

        c = U256.div(a, b)
        assert(c.to_int() == 2)

    def test_two(self):

        a = U256(11)
        b = U256(0)

        c = U256.div(a, b)
        assert(c.to_int() == 0)

class TestMod:

    def test_one(self):

        a = U256(5)
        b = U256(2)

        c = U256.mod(a, b)
        assert(c.to_int() == 1)

    def test_two(self):

        a = U256(3)
        b = U256(6)

        c = U256.mod(a, b)
        assert(c.to_int() == 3)

    def test_three(self):

        a = U256(1)
        b = U256(0)

        c = U256.mod(a, b)
        assert(c.to_int() == 0)

class TestAddMod:

    def test_one(self):

        a = U256(3)
        b = U256(2)
        c = U256(6)

        d = U256.addmod(a, b, c)
        assert(d.to_int() == 5)

    def test_two(self):

        a = U256(11)
        b = U256(9)
        c = U256(10)

        d = U256.addmod(a, b, c)
        assert(d.to_int() == 0)

    def test_three(self):

        a = U256(1)
        b = U256(3)
        c = U256(0)

        d = U256.addmod(a, b, c)
        assert(d.to_int() == 0)

class TestSdiv:

    def test_one(self):

        a = U256.from_signed_integer(-1)
        b = U256.from_signed_integer(-1)

        c = U256.sdiv(a, b)
        assert(c.to_signed_int() == 1)

    def test_two(self):

        a = U256.from_signed_integer(5)
        b = U256.from_signed_integer(0)

        c = U256.sdiv(a, b)
        assert(c.to_int() == 0)

    def test_three(self):

        a = U256.from_signed_integer(-13)
        b = U256.from_signed_integer(4)
        
        c = U256.sdiv(a, b)
        assert(c.to_signed_int() == -3)
    
class TestSmod:

    def test_one(self):

        a = U256.from_signed_integer(-5)
        b = U256.from_signed_integer(2)

        c = U256.smod(a, b)
        assert(c.to_signed_int() == -1)

    def test_two(self):

        a = U256.from_signed_integer(1)
        b = U256.from_signed_integer(0)

        c = U256.smod(a, b)
        assert(c.to_signed_int() == 0)
class TestMulmod:

    def test_one(self):

        a = U256(6)
        b = U256(7)
        c = U256(30)

        d = U256.mulmod(a, b, c)
        assert(d.to_int() == 12)

    def test_two(self):

        a = U256(1)
        b = U256(1)
        c = U256(0)

        d = U256.mulmod(a, b, c)
        assert(d.to_int() == 0)

class TestExp:

    def test_one(self):

        a = U256(2)
        b = U256(3)

        c = U256.exp(a, b)
        assert(c.to_int() == 8)

    def test_two(self):

        a = U256(2**128)
        b = U256(2)

        c = U256.exp(a, b)
        assert(c.to_int() == 0)

class TestSignExtend:

    def test_one(self): 

        b = U256.from_signed_integer(1)
        x = U256.from_signed_integer(16)

        c = U256.sign_extend(b, x)
        assert(c.to_signed_int() == 16)

    def test_two(self):

        b = U256.from_signed_integer(0)
        x = U256.from_signed_integer(255)

        c = U256.sign_extend(b, x)
        assert(c.to_signed_int() == -1)

    def test_three(self):

        b = U256.from_signed_integer(1)
        x = U256.from_signed_integer(65535)

        c = U256.sign_extend(b, x)
        assert(c.to_signed_int() == -1)

    def test_four(self):

        b = U256.from_signed_integer(0)
        x = U256.from_signed_integer(127)

        c = U256.sign_extend(b, x)
        assert(c.to_signed_int() == 127)

    def test_five(self):

        b = U256.from_signed_integer(0)
        x = U256.from_signed_integer(257)

        c = U256.sign_extend(b, x)
        assert(c.to_signed_int() == 1)
from src.data import EVMMemory, EVMMemoryReturnValue
from src.utils.u256 import U256
from src.utils.exceptions import *
import pytest

class TestMemoryMethods:

    class TestStore:

        def test_one(self):

            mem = EVMMemory()

            value = U256(2**255 - 1)
            with pytest.raises(EVMInvalidMemoryInput):
                mem.store(0, value)

        def test_two(self):

            mem = EVMMemory()

            offset = U256(0)
            value = 2**256 - 1

            with pytest.raises(EVMInvalidMemoryInput):
                mem.store(offset, value)

        def test_three(self):

            mem = EVMMemory()

            offset = 0
            value = 2**256 - 1

            with pytest.raises(EVMInvalidMemoryInput):
                mem.store(offset, value)

        def test_four(self):

            mem = EVMMemory()
            offset = U256(0)
            value = U256(2**256 - 1)
            
            mem.store(offset, value)

            assert_value = ""

            for i in range(32):

                assert_value += mem._memory[i]

            assert(assert_value == "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")

        def test_five(self):

            mem = EVMMemory()
            offset = U256(0)
            value = U256(255)

            mem.store(offset, value)

            assert_value = ""

            for i in range(32):

                try:
                    assert_value += mem._memory[i]
                except KeyError:
                    assert_value += "00"

            assert(assert_value == "00000000000000000000000000000000000000000000000000000000000000ff")

        def test_six(self):

            mem = EVMMemory()
            offset = U256(1)
            value = U256(255)

            mem.store(offset, value)

            assert_value = ""

            for i in range(32):

                try:
                    assert_value += mem._memory[i+1]
                except KeyError:
                    assert_value += "00"

            assert(assert_value == "00000000000000000000000000000000000000000000000000000000000000ff")

        def test_six(self):

            mem = EVMMemory()
            offset = U256(2**253 - 1 - 31)
            value = U256(2**256 - 1)

            with pytest.raises(EVMMemoryOffsetTooLarge):

                mem.store(offset, value)

    class TestLoad:

        def test_one(self):

            mem = EVMMemory()
            offset = "1"

            with pytest.raises(EVMInvalidMemoryInput):

                mem.load(offset)

        def test_two(self):

            mem = EVMMemory()
            offset = U256(0)

            value = mem.load(offset)
            assert(value._value.to_int() == 0)

        def test_three(self):

            mem = EVMMemory()
            offset = U256(0)

            value = mem.load(offset)
            assert(value._value.to_int() == 0)

        def test_four(self):

            mem = EVMMemory()
            mem.store(U256(0), U256(2**256 - 1))

            value = mem.load(U256(0))
            assert(value._value.to_int() == 2**256 - 1)

        def test_five(self):

            mem = EVMMemory()
            mem.store(U256(0), U256(255))

            value = mem.load(U256(0))
            assert(value._value.to_int() == 255)

        def test_six(self):

            mem = EVMMemory()

            for i in range(32):

                mem._memory[i] = "ff"

            value = mem.load(U256(1))


            print(value._value.to_int())

            assert(value._value.to_int() == 115792089237316195423570985008687907853269984665640564039457584007913129639680)

    class TestStoreCustom:

        def test_one(self):

            mem = EVMMemory()
            
            offset = 0
            length = U256(1)
            value = "ff"

            with pytest.raises(EVMInvalidMemoryInput):

                mem.store_custom(offset, length, value)

        def test_two(self):

            mem = EVMMemory()
            
            offset = U256(0)
            length = 1
            value = "ff"

            with pytest.raises(EVMInvalidMemoryInput):

                mem.store_custom(offset, length, value)

        def test_three(self):

            mem = EVMMemory()
            
            offset = U256(0)
            length = U256(1)
            value = U256(255)

            with pytest.raises(EVMInvalidMemoryInput):

                mem.store_custom(offset, length, value)

        def test_four(self):

            mem = EVMMemory()
            
            offset = U256(0)
            length = U256(2)
            value = "ff"

            with pytest.raises(EVMMemoryInputLengthInconsistency):

                mem.store_custom(offset, length, value)

        def test_five(self):

            mem = EVMMemory()

            offset = U256(0)
            length = U256(1)
            value = "ff"

            mem.store_custom(offset, length, value)

            assert(mem._memory[0] == "ff")

        def test_six(self):

            mem = EVMMemory()

            offset = U256(0)
            length = U256(1)
            value = "FF"

            mem.store_custom(offset, length, value)

            assert(mem._memory[0] == "ff")

        def test_seven(self):

            mem = EVMMemory()

            offset = U256(0)
            length = U256(33)
            value = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

            mem.store_custom(offset, length, value)

            assert_value = ""

            for i in range(33):

                assert_value += mem._memory[i]

            assert(assert_value == "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")

        def test_eight(self):

            mem = EVMMemory()

            offset = U256(2**253 - 1 - 32)
            length = U256(34)
            value = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

            with pytest.raises(EVMMemoryOffsetTooLarge):

                mem.store_custom(offset, length, value) 

    class TestLoadCustom:
        
        def test_one(self):

            mem = EVMMemory()
            offset = 0
            length = U256(64)

            with pytest.raises(EVMInvalidMemoryInput):

                mem.load_custom(offset, length)

        def test_two(self):

            mem = EVMMemory()
            offset = U256(0)
            length = 64

            with pytest.raises(EVMInvalidMemoryInput):

                mem.load_custom(offset, length)

        def test_three(self):

            mem = EVMMemory()
            for i in range(32):

                mem._memory[i] = "ff"

            offset = U256(0)
            length = U256(32)

            return_val = mem.load_custom(offset, length)
            assert(return_val._value == "ff" * 32)

        def test_four(self):

            mem = EVMMemory()

            for i in range(32):

                mem._memory[i] = "ff"

            offset = U256(0)
            length = U256(33)

            return_val = mem.load_custom(offset, length)
            assert(return_val._value == "ff" * 32 + "00")

        def test_five(self):

            mem = EVMMemory()

            offset = U256(2**253 - 1)
            length = U256(2)

            with pytest.raises(EVMMemoryOffsetTooLarge):

                mem.load_custom(offset, length)

    class TestSize:

        def test_one(self):

            mem = EVMMemory()

            assert(mem.get_size().to_int() == 0)

        def test_two(self):

            mem = EVMMemory()

            mem.store(U256(0), U256(2**256 - 1))

            assert(mem.get_size().to_int() == 31)

from src.data import EVMStack
from src.utils.u256 import U256
from src.utils.exceptions import *
import pytest

class TestStackMethods:

    class TestPush:

        def test_one(self):

            stack = EVMStack()
            value = U256(1)

            stack.push(value)
            assert(
                stack._stack[0].to_int() == 1
                )

        def test_two(self):

            stack = EVMStack()
            value = 1

            with pytest.raises(EVMStackInvalidInputType):

                stack.push(value)

        def test_three(self):

            stack = EVMStack()
            value = "12"

            with pytest.raises(EVMStackInvalidInputType):

                stack.push(value)

        def test_four(self):

            stack = EVMStack()

            for i in range(1024):

                stack.push(U256(i))

            value = U256(1)

            with pytest.raises(EVMStackOverFlow):

                stack.push(value)

        def test_five(self):

            stack = EVMStack()
            
            stack.push(U256(1))
            stack.push(U256(2))

            assert(
                stack._stack[1].to_int() == 1
            )

    class TestPop:

        def test_one(self):

            stack = EVMStack()
            
            stack.push(U256(1))
            value = stack.pop()

            assert(value.to_int() == 1)

        def test_two(self):

            stack = EVMStack()

            stack.push(U256(3))
            stack.push(U256(4))

            value = stack.pop()
            assert(value.to_int() == 4)

        def test_three(self):

            stack = EVMStack()

            stack.push(U256(1))
            stack.push(U256(2))
            stack.push(U256(3))

            value = stack.pop()
            assert(value.to_int() == 3)

        def test_four(self):

            stack = EVMStack()
            
            with pytest.raises(EVMEmptyStack):

                stack.pop()

    class TestDup():

        def test_one(self):

            stack = EVMStack()

            with pytest.raises(EVMInvalidStackIndex):

                stack.dup(33)

        def test_two(self):

            stack = EVMStack()

            with pytest.raises(EVMStackItemEmpty):

                stack.dup(1)

        def test_three(self):

            stack = EVMStack()

            stack.push(U256(8))

            stack.dup(1)
            with pytest.raises(EVMInvalidStackIndex):

                stack.dup(0)

        def test_four(self):

            stack = EVMStack()

            stack.push(U256(99))
            stack.dup(1)

            assert(
                stack._stack[0].to_int() == 99 and stack._stack[1].to_int() == 99
            )

    class TestSwap():

        def test_one(self):

            stack = EVMStack()

            stack.push(U256(1))
            stack.push(U256(2))

            stack.swap(1)
            assert(
                stack._stack[0].to_int() == 1 and stack._stack[1].to_int() == 2
            )

        def test_two(self):

            stack = EVMStack()

            stack.push(U256(1))
            stack.push(U256(2))
            stack.push(U256(3))

            stack.swap(2)

            assert(
                stack._stack[0].to_int() == 1 and stack._stack[2].to_int() == 3
            )

        def test_three(self):

            stack = EVMStack()

            with pytest.raises(EVMEmptyStack):
                stack.swap(2)

        def test_four(self):

            stack = EVMStack()
            stack.push(U256(11))

            with pytest.raises(EVMStackItemEmpty):

                stack.swap(12)

        def test_five(self):

            stack = EVMStack()
            for i in range(16):
                stack.push(U256(i))

            with pytest.raises(EVMInvalidStackDupIndex):
                stack.swap(17)
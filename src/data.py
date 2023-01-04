"""
Module containg the stack and memory data structures for the EVM
"""
from utils.u256 import *
from EVMErrors import *

class EVMMemory():

    # Each cell is 8 bits
    # Memory is byte-based

    def __init__(self):

        # Keys are addressed PER BYTE
        # Values are HEX STRINGS
        self._memory = {}
        self._farthest_address = 0

    def load(self, offset: U256) -> U256:

        offset_val = offset.to_int()
        loaded_value_str = ""
        for i in range(32):
            try:
                loaded_value_str = loaded_value_str + self._memory[offset_val + i] 
            except:
                loaded_value_str = loaded_value_str + "00"

        loaded_value_int = int(loaded_value_str, 16)
        return U256(loaded_value_int)

    def load_custom(self, offset: U256, length: U256) -> str:
        """
        Functions that allows for values of arbitrary length to be loaded from
        memory 
        
        Since value is not guaranteed to be within the bounds of the U256 type,
        a hexadecimal string is returned
        """
        offset_val = offset.to_int()
        loaded_value_str = ""
        for i in range(length):
            try:
                loaded_value_str = loaded_value_str + self._memory[offset_val + i] 
            except:
                loaded_value_str = loaded_value_str + "00"

        return loaded_value_str

    def store(self, offset: U256, value: U256):

        value_hex_str = value.to_hex_string()
        chopped_value_list = []
        offset_val = offset.to_int()
        for i in range(32):
            # Slice up 32-char hex string
            chopped_value_list.append(value_hex_str[i*2:(i*2)+2])

        for i in range(32):

            self._memory[offset_val + i] = chopped_value_list[i]
            if offset_val + i > self._farthest_address:
                self._farthest_address = offset_val

    def print(self):

        print("CURRENT EVM MEMORY:")

        farthest_multiple = self._farthest_address % 32

        for nth_word in range(farthest_multiple + 1):

            word = ""

            for jth_bit in range(32):
                try:
                    # Value exists
                    word += self._memory[jth_bit + (nth_word * 32)]
                except KeyError: 
                    # Default to '00'
                    word += "00"

            word_address = f"[{hex(32 * nth_word)}]"
            print(f"{word_address} {word}")

        # print(self._memory)
        print("--------")

    def size(self):
        """
        Returns the highest address that has been accessed
        """
        pass


class EVMStack():

    def __init__(self):

        self._stack = []

    def push(self, item: U256):
        
        if (len(self._stack) + 1 > 1024):

            raise EVMStackOverFlow()

        self._stack.insert(0, item)

    def pop(self) -> U256:

        return self._stack.pop()

    def print(self):

        print("CURRENT EVM STACK:")
        counter = 0
        for i in range(len(self._stack)):
            print(f"[{hex(counter)}] {self._stack[i]}")
            counter += 32

    def get_item(self, index: U256):

        if index.to_int() > 1024:
            raise EVMOutsideStackBounds(index.to_int())

        try:
            return self._stack[index.to_int()].deepcopy()
        except:
            raise EVMUndefinedStackItem(index.to_int())

    def replace(self, index: U256, new_value: U256) -> U256:

        if index.to_int() > 1024:
            raise EVMOutsideStackBounds(index.to_int())

        if len(self._stack) < index:
            raise EVMOutsideStackBounds(index.to_int())

        self._stack[index] = new_value
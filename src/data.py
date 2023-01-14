"""
Module containg the stack and memory data structures for the EVM
"""
from .utils.u256 import *
from math import floor
from copy import deepcopy
from .utils.exceptions import *
import copy

class EVMMemoryReturnValue():
    """
    Class that acts as the return object of every interaction with EVMMemory

    EVMMemoryReturnValue contains two attributes: _value is the actual return
    value of the interaction with memory while _mem_expansion_cost is an
    optional attribute that represents the gas cost of the memory expansion of
    the operation  
    """

    def __init__(self, value = None, mem_expansion_cost: int = 0):

        # If load, value from memory
        self._value = value
        # Highest referenced memory address in bytes
        self._mem_expansion_cost = mem_expansion_cost

    def get_value(self):

        return self._value

    def get_mem_expansion_cost(self):

        return self._mem_expansion_cost

class EVMMemory():
    """
    Class that serves to maintain the memory component of the EVM

    EVMMemory contains the _memory attribute which maps byte addresses (ints) to
    the values stored in those addresses (lowercase hex strings)

    Because of the complex nature of memory expansion and its associated gas
    costs, any read/write/other complex usage of memory returns an
    EVMMemoryReturnValue object
    """
    # Each cell is 8 bits
    # Memory is byte-based

    def __init__(self):

        # Keys are addressed PER BYTE
        # Values are HEX STRINGS
        self._memory = {}

        # Highest referenced memory address in bytes (int)
        self._size: int = 0

        # Number of 32-byte words required for memory 
        # (self._size + 31) // 32
        self._size_words: int = 0

    def get_size(self) -> U256:

        return U256(self._size)

    def get_mem_cost(self) -> int:
        """
        Memory Expansion Function from the Ethereum Yellowpaper
        get_mem_cost() returns the required amount of gas for memory expansion
        """
        return (3 * self._size_words) + floor((self._size_words ** 2) / 512)

    def load(self, offset: U256) -> EVMMemoryReturnValue:
        """
        Function that loads U256 value from memory and returns said value inside
        an EVMMemoryReturnValue object
        """

        prior_mem_cost = self.get_mem_cost()

        offset_val = offset.to_int()
        loaded_value_str = ""
        for i in range(32):
            try:
                loaded_value_str = loaded_value_str + self._memory[offset_val + i] 
            except:
                loaded_value_str = loaded_value_str + "00"

        farthest_address = offset_val + 31

        if farthest_address > self._size:
            # Need to update farthest referenced address
            self._size = farthest_address
            self._size_words = (farthest_address + 31) // 32

        curr_mem_cost = self.get_mem_cost()

        mem_exp_cost = curr_mem_cost - prior_mem_cost

        loaded_value_int = int(loaded_value_str, 16)

        # return U256(loaded_value_int)
        return EVMMemoryReturnValue(U256(loaded_value_int), mem_exp_cost)

    def load_custom(self, offset: U256, length: U256) -> EVMMemoryReturnValue:
        """
        Functions that allows for values of arbitrary length to be loaded from
        memory 
        
        Since value is not guaranteed to be within the bounds of the U256 type,
        a hexadecimal string is returned
        """
        prior_mem_cost = self.get_mem_cost()

        offset_val = offset.to_int()
        loaded_value_str = ""
        for i in range(length):
            try:
                loaded_value_str = loaded_value_str + self._memory[offset_val + i] 
            except:
                loaded_value_str = loaded_value_str + "00"

        farthest_address = offset_val + length.to_int() - 1

        if farthest_address > self._size:
            
            self._size = farthest_address
            self._size_words = (farthest_address + 31) // 32

        curr_mem_cost = self.get_mem_cost()

        mem_exp_cost = curr_mem_cost - prior_mem_cost

        return EVMMemoryReturnValue(loaded_value_str, mem_exp_cost)

    def store(self, offset: U256, value: U256) -> EVMMemoryReturnValue:
        """
        Store U256 value into memory
        """
        prior_mem_cost = self.get_mem_cost()

        value_hex_str = value.to_hex_string()
        chopped_value_list = []
        offset_val = offset.to_int()
        for i in range(32):
            # Slice up 32-char hex string
            chopped_value_list.append(value_hex_str[i*2:(i*2)+2])

        for i in range(32):

            self._memory[offset_val + i] = chopped_value_list[i]

        farthest_address = offset_val + 31

        if farthest_address > self._size:
            self._size = farthest_address
            self._size_words = (farthest_address + 31) // 32

        curr_mem_cost = self.get_mem_cost()

        mem_exp_cost = curr_mem_cost - prior_mem_cost

        return EVMMemoryReturnValue(mem_expansion_cost= mem_exp_cost)

    def store_custom(self, offset: U256, length: U256, data: str) -> EVMMemoryReturnValue:
        """
        Stores data of arbitrary length into memory
        """
        
        prior_mem_cost = self.get_mem_cost()

        offset_val = offset.to_int()
        length_val = length.to_int()

        chopped_data_list = []

        for i in range(length_val):

            chopped_data_list.append(data[i*2:(i * 2) + 2])

        for i in range(length_val):

            self._memory[offset_val + i] = chopped_data_list[i]

        farthest_address = self._size + length - 1

        if farthest_address > self._size:
            self._size = farthest_address
            self._size_words = (farthest_address + 31) // 32

        curr_mem_cost = self.get_mem_cost()

        mem_exp_cost = curr_mem_cost - prior_mem_cost

        return EVMMemoryReturnValue(mem_expansion_cost= mem_exp_cost)

    def print(self):

        print("CURRENT EVM MEMORY:")

        farthest_multiple = self._size % 32

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

        print("--------")

    def size(self) -> U256:
        """
        Returns the highest address that stores a nonzero value in memory
        """
        return U256(self._size)


class EVMStack():

    def __init__(self):

        self._stack: list[U256] = []

    def push(self, item: U256):

        if not isinstance(item, U256):

            raise EVMStackInvalidInputType(item)
        
        if (len(self._stack) + 1 > 1024):

            raise EVMStackOverFlow()

        self._stack.insert(0, item)

    def pop(self) -> U256:

        if len(self._stack) == 0:

            raise EVMEmptyStack()

        return self._stack.pop(0)

    def print(self):

        print("CURRENT EVM STACK:")
        counter = 0
        for i in range(len(self._stack)):
            print(f"[{hex(counter)}] {self._stack[i]}")
            counter += 32

    def __get_item(self, index: int) -> U256:
        """
        Internal method that retrieves stack item from position

        Stack items are indexed starting with 1 (top of stack has index one, the
        item below that has index two, and so on)
        """
        if index < 1 or index > 32:

            raise EVMInvalidStackIndex()

        try:
            return self._stack[index - 1]
        except IndexError:
            raise EVMStackItemEmpty(index)

    def replace(self, index: U256, new_value: U256) -> U256:

        if index.to_int() > 1024:
            raise EVMOutsideStackBounds(index.to_int())

        if len(self._stack) < index:
            raise EVMOutsideStackBounds(index.to_int())

        self._stack[index] = new_value

    def insert(self, index: U256, value: U256):

        pass

    def dup(self, index: int):

        item_to_dup = self.__get_item(index)
        self._stack.insert(
            0,
            copy.deepcopy(item_to_dup)
        )

    def swap(self, index: int):

        if len(self._stack) == 0:
            raise EVMEmptyStack()
        elif index > 16:
            raise EVMInvalidStackDupIndex()
        elif len(self._stack) < index:
            raise EVMStackItemEmpty()

        self._stack[0], self._stack[index] = self._stack[index], self._stack[0]

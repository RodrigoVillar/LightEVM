"""
Module containing the ROM and Instruction classes
"""

from .utils.exceptions import *
from .utils.u256 import U256
from .utils.opcodes import get_readable_opcode, push_opcodes, dup_opcodes, swap_opcodes

class EVMInstruction():

    def __init__(self, hex: str, readable: str, metadata: str = None):
        self._hex_op = hex
        self._readable_op = readable
        # If PUSH operation, then metadata represents the data to push onto
        # stack
        # If DUP operation, then metadata represents the stack index to copy
        # If SWAP operation, then metadata represents the stack index to swap
        # with top element
        self._metadata = metadata

    def get_len(self):

        if self._metadata == None:
            return 1
        else:
            return 1 + int((len(self._metadata) / 2))

    def get_hex_code(self):
        return self._hex_op

    def get_readable_op(self):
        return self._readable_op

    def get_metadata(self):
        return self._metadata

    def __str__(self) -> str:
        if self._metadata == None:
            return self._readable_op 
        else:
            return self._readable_op + " " + self._metadata

class EVMRom():

    def __init__(self, bytecode: str):

        self._rom = {}
        self._size = 0
        self._farthest_address = 0

        while len(bytecode) != 0:

            op = bytecode[:2].upper()
            readable_op = get_readable_opcode(op)
            if op in push_opcodes:
                chars_selected = int(readable_op[4:]) * 2
                metadata = bytecode[2:2 + chars_selected]
                insn = EVMInstruction(op, readable_op, metadata) 
                bytecode = bytecode[2 + chars_selected:]   
            elif op in dup_opcodes:
                metadata = int(readable_op[3:])
                insn = EVMInstruction(op, readable_op, metadata)
                bytecode = bytecode[2:]
            elif op in swap_opcodes:
                metadata = int(readable_op[4:])
                insn = EVMInstruction(op, readable_op, metadata)
                bytecode = bytecode[2:]
            else:
                insn = EVMInstruction(op, readable_op)
                bytecode = bytecode[2:]

            self._rom[self._size] = insn
            self._farthest_address = self._size
            self._size += insn.get_len()

    def get_insn(self, line: int) -> EVMInstruction:

        try:
            return self._rom[line]
        except:
            raise EVMInstructionNotFound()

    def get_size(self) -> int:

        return self._size

    def is_end_of_program(self, pc : int) -> bool:

        print(f"size is :{self._size} while pc is {pc}")
        return self._farthest_address < pc

    def get_code(self, offset: U256, length: U256) -> str:

        pass

"""
Module containining all EVM functionality
"""
from EVMErrors import *
from utils.u256 import *
import EVMOpcodes
from utils import operations
from data import EVMMemory, EVMStack
from transaction import EVMMessage, EVMTransaction
from block import EVMBlock
from state import EVMGlobalState, EVMStorage
from bytecode import EVMInstruction, EVMRom

class EVMInput():

    def initialize_from_toml(self, toml_dict: dict):

        self._chain_id = toml_dict["chain"]["chain_id"]
        self._timestamp = toml_dict["block"]["timestamp"]
        self._difficulty = toml_dict["block"]["difficulty"]

class EVM():

    def __init__(self, input: EVMInput):

        self._stack = EVMStack()
        self._memory = EVMMemory()
        self._pc = 0
        self._storage = EVMStorage()
        self._gas = 0
        # Maps integers to instructions
        self._rom = EVMRom("")
        self._stop = False

        self._tx = EVMTransaction()

        self._msg = EVMMessage()

        self._next_insn_slot = 0

        self._current_block = EVMBlock()

        self._state = EVMGlobalState()

    def insert_insn(self, insn: EVMInstruction):

        self._rom[self._next_insn_slot] = insn
        self._next_insn_slot += insn.get_len()

    def print_rom(self):

        print("EVM ROM:")
        for i in range(self._next_insn_slot):
            try:
                print(f"[{hex(i)}] {str(self._rom[i])}")
            except:
                continue

    def print_stack(self):

        self._stack.print()

    def print_memory(self):

        self._memory.print()

    def execute_insn(self, insn: EVMInstruction):

        operations.match_insn(self, insn)

        if self._rom.is_end_of_program(self._pc):
            self._stop = True
        self.print_stack()
        self.print_memory()

    def run(self):

        # Deduct base gas fee of 21000
        self._gas -= 21000

        while not self._stop:
            # Grab instruction from ROM
            print(f"Current PC: [{self._pc}]")
            insn = self._rom[self._pc]
            print(f"Current Instruction: {insn}")
            print(f"Current Gas: {self._gas}")
            self.execute_insn(insn)

def initialize_from_toml(evm: EVM, toml: dict):

    pass

class EVMInterpreter():

    def __init__(self, toml_dict = None):

        self._evm = EVM(100000)
        if toml_dict != None:
            initialize_from_toml(self._evm)


    def interpret(self, bytecode: str):

        while len(bytecode) != 0:
            op = bytecode[:2].upper()
            readable_op = EVMOpcodes.get_readable_opcode(op)
            if op in EVMOpcodes.push_opcodes:
                chars_selected = int(readable_op[4:]) * 2
                metadata = bytecode[2:2 + chars_selected]
                insn = EVMInstruction(op, readable_op, metadata) 
                bytecode = bytecode[2 + chars_selected:]   
            elif op in EVMOpcodes.dup_opcodes:
                metadata = int(readable_op[3:])
                insn = EVMInstruction(op, readable_op, metadata)
                bytecode = bytecode[2:]
            elif op in EVMOpcodes.swap_opcodes:
                metadata = int(readable_op[4:])
                insn = EVMInstruction(op, readable_op, metadata)
                bytecode = bytecode[2:]
            else:
                insn = EVMInstruction(op, readable_op)
                bytecode = bytecode[2:]

            self._evm.insert_insn(insn)

    def run_evm(self):

        self._evm.run()

    def print_state(self):

        self._evm.print_rom()
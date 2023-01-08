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
from utils.input import EVMInput
from utils.address import EVMAddress


class EVMReturnFrame():

    pass

class EVM():

    def __init__(self, input: EVMInput):

        # Stack empty at initialization
        self._stack = EVMStack()
        # Memory empty at initialization
        self._memory = EVMMemory()
        # Program Counter
        self._pc = 0
        # Storage derived from input
        self._storage = input.get_storage()
        # Gas limit derived from input
        self._gas = input.get_tx_gas_limit()
        # Bytecode derived from input
        self._rom = EVMRom(
            self._storage.get_contract_bytecode(input.get_to())
            )

        self._stop = False

        self._tx = EVMTransaction(
            input.get_tx_type(),
            input.get_gas_price(),
            input.get_tx_gas_limit(),
            input.get_from()
        )

        self._msg = EVMMessage(
            input.get_calldata(),
            input.get_signature(),
            input.get_value(),
            input.get_to()
        )

        self._current_block = EVMBlock(
            input.get_base_fee(),
            input.get_block_number(),
            input.get_block_gas_limit(),
            input.get_coinbase(), 
            input.get_timestamp(),
            input.get_difficulty()
        )

        self._state = EVMGlobalState(
            input.get_chain_id()
        )

        self._return_data = ""

    def print_rom(self):

        print("EVM ROM:")
        for i in range(self._rom.get_size()):
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

class EVMInterpreter():

    def __init__(self, input: EVMInput):

        self._evm = EVM(input)

    def run_evm(self):

        self._evm.run()

"""
Top level file that controls the VM environment and process
"""

from .evm import EVM
from .input import EVMInput
from .bytecode import EVMInstruction
from .utils.operations import match_insn

class EVMInterpreter():

    def __init__(self, input: EVMInput):

        self._evm = EVM(input)

    def run_evm(self):

        while not self._evm._stop:

            insn_to_execute = self._evm.grab_insn()

            match_insn(self._evm, insn_to_execute)

            self._evm.print_stack()
            self._evm.print_memory()

            if self._evm._rom.is_end_of_program(self._evm._pc):

                self._evm._stop = True



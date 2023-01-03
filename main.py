import EVMOpcodes
from evm import EVMInterpreter
import sys

class OpCode():

    def __init__(self, code: str, arg = None):

        self._code = code
        self._arg = arg

    def get_string(self):

        if self._arg != None:
            return self._code + " " + self._arg
        else:
            return self._code


class ReadableStack():

    def __init__(self):
        
        self._stack = []

    def push(self, opcode: OpCode):

        self._stack.append(opcode)

    def print(self):

        for i in self._stack:
            print(i.get_string())


if __name__ == "__main__":
    program = EVMInterpreter()
    # bytecode = input("Please input the contract bytecode, STARTING WITH 0x: ")
    bytecode = sys.argv[1]

    # Formatting
    bytecode.strip()
    bytecode.lower()
    bytecode = bytecode[2:]

    program.interpret(bytecode)
    program.run_evm()
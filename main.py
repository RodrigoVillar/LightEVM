import EVMOpcodes
from evm import EVMInterpreter
import sys, toml

if __name__ == "__main__":

    with open("./execution.toml", "r"):

        toml_dict = toml.load(f)

    program = EVMInterpreter(toml_dict=toml_dict)
    
    bytecode = sys.argv[1]

    # Formatting
    bytecode.strip()
    bytecode.lower()
    bytecode = bytecode[2:]

    program.interpret(bytecode)
    program.run_evm()
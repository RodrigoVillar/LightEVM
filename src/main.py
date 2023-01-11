from input import EVMInput
from interpreter import EVMInterpreter
import sys, toml
from dotenv import dotenv_values

if __name__ == "__main__":

    with open("../execution.toml", "r") as f:

        toml_dict = toml.load(f)
        f.close()

    evm_input = EVMInput()
    evm_input.from_toml(toml_dict)

    program = EVMInterpreter(evm_input)

    program.run_evm()
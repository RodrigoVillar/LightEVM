from utils.input import EVMInput
from evm import EVMInterpreter
import sys, toml
from dotenv import dotenv_values

if __name__ == "__main__":

    with open("./execution.toml", "r") as f:

        toml_dict = toml.load(f)
        f.close()

    evm_input = EVMInput(toml_dict)

    program = EVMInterpreter(toml_dict=toml_dict)

    program.run_evm()
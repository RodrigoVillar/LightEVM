from src.input import EVMInput
from src.interpreter import EVMInterpreter
from dotenv import load_dotenv
import toml

if __name__ == "__main__":

    load_dotenv()

    with open("./execution.toml", "r") as f:

        toml_dict = toml.load(f)
        f.close()

    evm_input = EVMInput()
    evm_input.from_toml(toml_dict)

    program = EVMInterpreter(evm_input)

    program.run_evm()
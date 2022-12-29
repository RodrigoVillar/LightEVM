"""
Module containining all EVM functionality
"""
from EVMErrors import *
from EVMUtils import *
import EVMOpcodes

class EVMGlobalState():

    def __init__(self):
        self._chain_id = None


class EVMTransaction():

    def __init__(self):

        self._caller = None
        self._origin = None
        self._value = None


class EVMMemory():

    # Each cell is 8 bits
    # Memory is byte-based

    def __init__(self):

        # Keys are addressed PER BYTE
        # Values are HEX STRINGS
        self._memory = {}
        self._farthest_address = 0

    def load(self, offset: U256) -> U256:

        offset_val = offset.to_int()
        loaded_value_str = ""
        for i in range(32):
            try:
                loaded_value_str = loaded_value_str + self._memory[offset_val + i] 
            except:
                loaded_value_str = loaded_value_str + "00"

        loaded_value_int = int(loaded_value_str, 16)
        return U256(loaded_value_int)
        

    def store(self, offset: U256, value: U256):

        value_hex_str = value.to_hex_string()
        chopped_value_list = []
        offset_val = offset.to_int()
        for i in range(32):
            # Slice up 32-charhex string
            chopped_value_list.append(value_hex_str[i*2:(i*2)+2])

        for i in range(32):

            self._memory[offset_val + i] = chopped_value_list[i]
            if offset_val + i > self._farthest_address:
                self._farthest_address = offset_val

    def print(self):

        print("CURRENT EVM MEMORY:")

        farthest_multiple = self._farthest_address % 32

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

        # print(self._memory)
        print("--------")


class EVMStack():

    def __init__(self):

        self._stack = []

    def push(self, item: U256):
        
        if (len(self._stack) + 1 > 1024):

            raise EVMStackOverFlow()

        self._stack.insert(0, item)

    def pop(self) -> U256:

        return self._stack.pop()

    def print(self):

        print("CURRENT EVM STACK:")
        counter = 0
        for i in range(len(self._stack)):
            print(f"[{hex(counter)}] {self._stack[i]}")
            counter += 32

    def get_item(self, index: U256):

        if index.to_int() > 1024:
            raise EVMOutsideStackBounds(index.to_int())

        try:
            return self._stack[index.to_int()].deepcopy()
        except:
            raise EVMUndefinedStackItem(index.to_int())

    def replace(self, index: U256, new_value: U256) -> U256:

        if index.to_int() > 1024:
            raise EVMOutsideStackBounds(index.to_int())

        if len(self._stack) < index:
            raise EVMOutsideStackBounds(index.to_int())

        self._stack[index] = new_value

class EVMInstruction():

    def __init__(self, hex: str, readable: str, metadata = None):
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

class EVMStorage():

    def __init__(self):

        # MAPS U256 to U256
        self._storage = {}

    def get(self, key: U256) -> U256:

        pass

    def store(self, key: U256, value: U256):

        pass


class EVM():

    def __init__(self, gas: int):

        self._stack = EVMStack()
        self._memory = EVMMemory()
        self._pc = 0
        self._storage = EVMStorage()
        self._gas = gas
        # Maps integers to instructions
        self._rom = {}
        self._tx_data = None
        self._stop = False

        self._next_insn_slot = 0

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

        insn_hex_code = insn.get_hex_code()
        insn_gas_cost = EVMOpcodes.get_opcode_gas(insn_hex_code)
        if self._gas - insn_gas_cost < 0:

            raise EVMOutOfGasError()

        self._gas -= insn_gas_cost

        # DO EXECUTION LOGIC HERE

        if (insn.get_readable_op()[:4] == "PUSH"): # PUSH OPERATION
            item = U256(int(insn.get_metadata(), 16))
            self._stack.push(item)
            self._pc += insn.get_len()
        elif (insn.get_readable_op()[:3] == "DUP"): # DUP OPERATION
            index = U256(insn.get_metadata())
            item_to_dup = self._stack.get_item(index)
            self._stack.push(item_to_dup)
        elif (insn.get_readable_op()[:4] == "SWAP"): # SWAP OPERATION
            index = U256(insn.get_metadata() + 1)
            new_a = self._stack.get_item(index)
            new_b = self._stack.pop()
            self._stack.push(new_a)
            self._stack.replace(index, new_b)
        elif (insn_hex_code == "01"): # ADD OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            c = U256.add(a, b)
            self._stack.push(c)
            self._pc += 1
        elif (insn_hex_code == "02"): # MUL OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            c = U256.mul(a, b)
            self._stack.push(c)
            self._pc += 1
        elif (insn_hex_code == "00"): # STOP OPERATION
            self._stop = True
            self._pc += 1
        elif (insn_hex_code == "52"): # MSTORE OPERATION
            offset = self._stack.pop()
            value = self._stack.pop()
            self._memory.store(offset, value)
            self._pc += 1
        elif (insn_hex_code == "51"): # MLOAD OPERATION
            offset = self._stack.pop()
            value_from_memory = self._memory.load(offset)
            self._stack.push(value_from_memory)
            self._pc += 1
        elif (insn_hex_code == "56"): # JUMP OPERATION
            dest = self._stack.pop()
            dest_insn = self._rom[dest.to_int()]
            # Check if destination is JUMPDEST
            if dest_insn.get_hex_code() != "5B":
                raise EVMInvalidJumpDestination(dest_insn.get_hex_code())
            self._pc = dest.to_int()
        elif (insn_hex_code == "5B"): # JUMPDEST OPERATION
            self._pc += 1
        elif (insn_hex_code == "57"): # JUMPI OPERATION
            dest = self._stack.pop()
            condition = self._stack.pop()
            if condition.to_int(): # If condition is true
                dest_insn = self._rom[dest.to_int()]
                if dest_insn.get_hex_code() != "5B":
                    raise EVMInvalidJumpDestination(dest_insn.get_hex_code())
                self._pc = dest.to_int()
            else:
                self._pc += 1
        elif (insn_hex_code == "58"): # PC OPERATION
            self._stack.push(U256(self._pc))
            self._pc += 1
        elif (insn_hex_code == "5A"): # GAS OPERATION
            self._stack.push(U256(self._gas))
        elif insn_hex_code == "05": # SDIV OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.sdiv(a, b))
        elif insn_hex_code == "06": # MOD OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.mod(a, b))
        elif insn_hex_code == "07": # SMOD OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.smod(a, b))
        elif insn_hex_code == "08": # ADDMOD OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            N = self._stack.pop()
            self._stack.push(U256.addmod(a, b, N))
        elif insn_hex_code == "09": # MULMOD OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            N = self._stack.pop()
            self._stack.push(U256.mulmod(a, b, N))
        elif insn_hex_code == "0A": # EXP OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.exp(a, b))
        elif insn_hex_code == "0B": # SIGNEXTEND OPERATION
            b = self._stack.pop()
            x = self._stack.pop()
            self._stack.push(U256.sign_extend(b, x))
        elif insn_hex_code == "10": # LT OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.lt(a, b))
        elif insn_hex_code == "11": # GT OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.gt(a, b))
        elif insn_hex_code == "12": # SLT OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.slt(a, b))
        elif insn_hex_code == "13": # SGT OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.sgt(a, b))
        elif insn_hex_code == "14": # EQ OPERATION
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.eq(a, b))
        elif insn_hex_code == "15": # ISZERO OPERATION
            a = self._stack.pop()
            self._stack.push(U256.is_zero(a))
        elif insn_hex_code == "16": # AND
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.bitwise_and(a, b))
        elif insn_hex_code == "17": # OR
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.bitwise_or(a, b))
        elif insn_hex_code == "18": # XOR
            a = self._stack.pop()
            b = self._stack.pop()
            self._stack.push(U256.bitwise_xor(a, b))
        elif insn_hex_code == "19": # NOT
            a = self._stack.pop()
            self._stack.push(U256.bitwise_not(a))
        elif insn_hex_code == "1A": # BYTE
            i = self._stack.pop()
            x = self._stack.pop()
            self._stack.push(U256.byte(i, x))
        elif insn_hex_code == "1B": # SHL
            shift = self._stack.pop()
            value = self._stack.pop()
            self._stack.push(U256.shl(shift, value))
        elif insn_hex_code == "1C": # SHR
            shift = self._stack.pop()
            value = self._stack.pop()
            self._stack.push(U256.shr(shift, value))
        elif insn_hex_code == "1D": # SAR
            shift = self._stack.pop()
            value = self._stack.pop()
            self._stack.push(U256.sar(shift, value))
        elif insn_hex_code == "A0": # LOG0
            pass
        elif insn_hex_code == "A1": # LOG1
            pass
        elif insn_hex_code == "A2": # LOG2
            pass
        elif insn_hex_code == "A3": # LOG3
            pass
        elif insn_hex_code == "A4": # LOG4
            pass
        elif insn_hex_code == "F0": # CREATE
            pass
        elif insn_hex_code == "F1": # CALL
            pass
        elif insn_hex_code == "F2": # CALLCODE
            # UNKNOWN LOGIC
            pass
        elif insn_hex_code == "F3": # RETURN
            pass
        elif insn_hex_code == "F4": # DELEGATECALL
            pass
        elif insn_hex_code == "F5": # CREATE2
            pass
        elif insn_hex_code == "FA": # STATICCALL
            pass
        elif insn_hex_code == "FD": # REVERT
            pass
        elif insn_hex_code == "FD": # SELFDESTRUCT
            pass
        elif insn_hex_code == "59": # MEMSIZE
            pass
        elif insn_hex_code == "30": # ADDRESS
            pass
        elif insn_hex_code == "31": # BALANCE
            pass
        elif insn_hex_code == "32": # ORIGIN
            pass
        elif insn_hex_code == "33": # CALLER
            pass
        elif insn_hex_code == "34": # CALLVALUE
            pass
        elif insn_hex_code == "35": # CALLDATALOAD
            pass
        elif insn_hex_code == "36": # CALLDATASIZE
            pass
        elif insn_hex_code == "37": # CALLDATACOPY
            pass
        elif insn_hex_code == "38": # CODESIZE
            pass 
        elif insn_hex_code == "39": # CODECOPY
            pass
        elif insn_hex_code == "3A": # GASPRICE
            pass
        elif insn_hex_code == "3B": # EXTCODESIZE
            pass
        elif insn_hex_code == "3C": # EXTCODECOPY
            pass
        elif insn_hex_code == "3D": # RETURNDATASIZE
            pass
        elif insn_hex_code == "3E": # RETURNDATACOPY
            pass
        elif insn_hex_code == "3F": # EXTCODEHASH
            pass
        elif insn_hex_code == "40": # BLOCKHASH
            pass
        elif insn_hex_code == "41": # COINBASE
            pass
        elif insn_hex_code == "42": # TIMESTAMP
            pass
        elif insn_hex_code == "43": # NUMBER
            pass
        elif insn_hex_code == "44": # DIFFICULTY
            pass
        elif insn_hex_code == "45": # GASLIMIT
            pass
        elif insn_hex_code == "46": # CHAINID
            pass
        elif insn_hex_code == "47": # SELFBALANCE
            pass
        elif insn_hex_code == "48": # BASEFEE
            pass
        else:
            raise EVMOperationNotImplemented(insn_hex_code)

        if self._pc >= self._next_insn_slot:
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

    def __init__(self):

        self._evm = EVM(100000)

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
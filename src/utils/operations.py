"""
Module containing the logic for all EVM operations

Each function takes care of the associated stack, memory, program counter, and
gas 
"""

from evm import EVM, EVMInstruction
from u256 import U256
from gas import charge_gas
from hashing import keccak256
from exceptions import *

def stop(evm: EVM):

    evm._stop = True
    evm._pc += 1
    charge_gas(evm, "00")

def add(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.add(a, b))

    evm._pc += 1

    charge_gas(evm, "01")

def mul(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()    
    evm._stack.push(U256.mul(a, b))

    evm._pc += 1

    charge_gas(evm, "02")

def sub(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.sub(a, b))

    evm._pc += 1

    charge_gas(evm, "03")

def div(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.div(a, b))

    evm._pc += 1

    charge_gas(evm, "04")

def sdiv(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.div(a, b))

    evm._pc += 1

    charge_gas(evm, "05")

def mod(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.mod(a, b))

    evm._pc += 1

    charge_gas(evm, "06")

def smod(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.smod(a, b))

    evm._pc += 1

    charge_gas(evm, "07")

def addmod(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    N = evm._stack.pop()
    evm._stack.push(U256.addmod(a, b, N))

    evm._pc += 1

    charge_gas(evm, "08")

def mulmod(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    N = evm._stack.pop()
    evm._stack.push(U256.mulmod(a, b, N))

    evm._pc += 1

    charge_gas(evm, "09")

def exp(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.exp(a, b))

    evm._pc += 1

    binary_b = bin(b.to_int())[2:]
    charge_gas(evm, "0A", metadata = len(binary_b))

def signextend(evm: EVM):

    b = evm._stack.pop()
    x = evm._stack.pop()
    evm._stack.push(U256.sign_extend(b, x))

    evm._pc += 1

    charge_gas(evm, "0B")

def lt(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.lt(a, b))

    evm._pc += 1

    charge_gas(evm, "10")

def gt(evm: EVM): 

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.gt(a, b))

    evm._pc += 1

    charge_gas(evm, "11")

def slt(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.slt(a, b))

    evm._pc += 1

    charge_gas(evm, "12")

def sgt(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.sgt(a, b))

    evm._pc += 1

    charge_gas(evm, "13")

def eq(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.eq(a, b))

    evm._pc += 1

    charge_gas(evm, "14")

def iszero(evm: EVM):

    a = evm._stack.pop()
    evm._stack.push(U256.is_zero(a))

    evm._pc += 1

    charge_gas(evm, "15")

def bitwise_and(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.bitwise_and(a, b))

    evm._pc += 1

    charge_gas(evm, "16")

def bitwise_or(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.bitwise_or(a, b))

    evm._pc += 1

    charge_gas(evm, "17")

def bitwise_xor(evm: EVM):

    a = evm._stack.pop()
    b = evm._stack.pop()
    evm._stack.push(U256.bitwise_xor(a, b))

    evm._pc += 1

    charge_gas(evm, "18")

def bitwise_not(evm: EVM):

    a = evm._stack.pop()
    evm._stack.push(U256.bitwise_not(a))

    evm._pc += 1

    charge_gas(evm, "19")

def byte(evm: EVM):

    i = evm._stack.pop()
    x = evm._stack.pop()
    evm._stack.push(U256.byte(i, x))

    evm._pc += 1

    charge_gas(evm, "1A")

def shl(evm: EVM):

    shift = evm._stack.pop()
    value = evm._stack.pop()
    evm._stack.push(U256.shl(shift, value))

    evm._pc += 1

    charge_gas(evm, "1B")

def shr(evm: EVM):

    shift = evm._stack.pop()
    value = evm._stack.pop()
    evm._stack.push(U256.shr(shift, value))

    evm._pc += 1

    charge_gas(evm, "1C")

def sar(evm: EVM):

    shift = evm._stack.pop()
    value = evm._stack.pop()
    evm._stack.push(U256.sar(shift, value))

    evm._pc += 1

    charge_gas(evm, "1D")

def sha3(evm: EVM):

    # Pop items from stack
    offset = evm._stack.pop()
    length = evm._stack.pop()

    # Get value from memory
    value = evm._memory.load_custom(offset, length)

    word_len = (len(value) + 1) // 2 

    hashed_value = keccak256(hex = value)

    evm._stack.push(
        U256(int(hashed_value, 16))
    )

    evm._pc += 1

    charge_gas(evm, "20")

def address(evm: EVM):

    evm._stack.push(
        evm._msg.get_recipient()
    )

    evm._pc += 1

    charge_gas(evm, "30")

def balance(evm: EVM):

    address = evm._stack.pop()

    evm._stack.push(
        evm._state.get_account_balance(address)
    )

    evm._pc += 1

    charge_gas(evm, "31")

def origin(evm: EVM):

    evm._stack.push(
        evm._tx.get_origin()
    )

    evm._pc += 1

    charge_gas(evm, "32")

def caller(evm: EVM):

    evm._stack.push(
        evm._msg.get_sender()
    )

    evm._pc += 1

    charge_gas(evm, "33")

def callvalue(evm: EVM):

    evm._stack.push(
        evm._msg.get_value()
    )

    evm._pc += 1

    charge_gas(evm, "34")

def calldataload(evm: EVM):

    i = evm._stack.pop()

    evm._stack.push(
        evm._msg.load_data(i)
    )

    evm._pc += 1

    charge_gas(evm, "35")

def calldatasize(evm: EVM):

    evm._stack.push(
        evm._msg.get_data_size()
    )

    evm._pc += 1

    charge_gas(evm, "36")

def calldatacopy(evm: EVM):

    pass

def codesize(evm: EVM):

    evm._stack.push(
        evm._rom.get_size()
    )

    evm._pc += 1

    charge_gas(evm, "38")

def codecopy(evm: EVM):
    
    pass

def gasprice(evm: EVM):

    evm._stack.push(
        evm._tx.get_gas_price()
    )

    evm._pc += 1

    charge_gas(evm, "3A")

def extcodesize(evm: EVM):

    pass

def extcodecopy(evm: EVM):

    pass

def returndatasize(evm: EVM):

    pass

def returndatacopy(evm: EVM):

    pass

def extcodehash(evm: EVM):

    pass

def blockhash(evm: EVM):

    pass

def coinbase(evm: EVM):

    evm._stack.push(
        evm._current_block.get_coinbase()
    )

    evm._pc += 1

def timestamp(evm: EVM):

    evm._stack.push(
        evm._current_block.get_timestamp()
    )

    evm._pc += 1

def number(evm: EVM):

    evm._stack.push(
        evm._current_block.get_number()
    )

    evm._pc += 1

def difficulty(evm: EVM):

    evm._stack.push(
        evm._current_block.get_difficulty()
    )

    evm._pc += 1

def gaslimit(evm: EVM):

    evm._stack.push(
        evm._current_block.get_gas_limit()
    )

    evm._pc += 1

def chainid(evm: EVM):

    pass

def selfbalance(evm: EVM):

    pass

def basefee(evm: EVM):

    pass

def pop(evm: EVM):

    evm._stack.pop()

    evm._pc += 1

    charge_gas(evm, "50")

def mload(evm: EVM):

    offset = evm._stack.pop()
    evm._stack.push(
        evm._memory.load(offset)
    )

    evm._pc += 1

    charge_gas(evm, "51")

def mstore(evm: EVM):

    offset = evm._stack.pop()
    value = evm._stack.pop()

    evm._memory.store(offset, value)

    evm._pc += 1

    charge_gas(evm, "52")

def mstore8(evm: EVM):

    offset = evm._stack.pop()
    value = evm._stack.pop()

    offset = U256.bitwise_and(offset, U256(255))

    evm._memory.store(offset, value)

    evm._pc += 1

    charge_gas(evm, "53")

def sload(evm: EVM):

    pass

def sstore(evm: EVM):

    pass

def jump(evm: EVM):

    destination = evm._stack.pop()
    assoc_insn = evm._rom.get_insn(destination.to_int())
    if assoc_insn != "5B":

        raise EVMInvalidJumpDesination(destination.to_int())

    evm._pc = destination.to_int()

    charge_gas(evm, "56")

def jumpi(evm: EVM):

    destination = evm._stack.pop()
    condition = evm._stack.pop()

    if condition.to_int() == 0:
        evm._pc += 1
    else:
        assoc_insn = evm._rom.get_insn(destination.to_int())
        
        if assoc_insn != "5B":

            raise EVMInvalidJumpDesination(destination.to_int())

        evm._pc = destination.to_int()

    charge_gas(evm, "57")

def pc(evm: EVM):

    evm._stack.push(
        evm._pc
    )

    evm._pc += 1

    charge_gas(evm, "58")

def msize(evm: EVM):

    pass

def gas(evm: EVM):

    pass

def jumpdest(evm: EVM):

    pass

def push(evm: EVM, bytes_to_push: int):

    pass

def dup(evm: EVM, index_to_dup: int):

    pass

def swap(evm: EVM, index_to_swap: int):

    pass

def log0(evm: EVM):

    pass

def log1(evm: EVM):

    pass

def log2(evm: EVM):

    pass

def log3(evm: EVM):

    pass

def log4(evm: EVM):

    pass

def create(evm: EVM):

    pass

def call(evm: EVM):

    pass

def callcode(evm: EVM):

    pass

def return_op(evm: EVM):

    pass

def delegatecall(evm: EVM):

    pass

def create2(evm: EVM):

    pass

def staticcall(evm: EVM):

    pass

def revert(evm: EVM):

    pass

def selfdestruct(evm: EVM):

    pass

def match_insn(evm: EVM, insn: EVMInstruction):
    """
    Function reponsible for matching EVM instruction to associated function
    """
    readable_insn = insn.get_readable_op()
    hex_insn = insn.get_hex_code()

    if hex_insn == "00":
        stop(evm)
    elif hex_insn == "01":
        add(evm)
    elif hex_insn == "02":
        mul(evm)
    elif hex_insn == "03":
        sub(evm)
    elif hex_insn == "04":
        div(evm)
    elif hex_insn == "05":
        sdiv(evm)
    elif hex_insn == "06":
        mod(evm) 
    elif hex_insn == "07":
        smod(evm)
    elif hex_insn == "08":
        addmod(evm)
    elif hex_insn == "09":
        mulmod(evm)
    elif hex_insn == "0A":
        exp(evm)
    elif hex_insn == "0B":
        signextend(evm)
    elif hex_insn == "10":
        lt(evm)
    elif hex_insn == "11":
        gt(evm)
    elif hex_insn == "12":
        slt(evm)
    elif hex_insn == "13":
        sgt(evm)
    elif hex_insn == "14":
        eq(evm)
    elif hex_insn == "15":
        iszero(evm)
    elif hex_insn == "16":
        bitwise_and(evm)
    elif hex_insn == "17":
        bitwise_or(evm)
    elif hex_insn == "18":
        bitwise_xor(evm)
    elif hex_insn == "19":
        bitwise_not(evm)
    elif hex_insn == "1A":
        byte(evm)
    elif hex_insn == "1B":
        shl(evm)
    elif hex_insn == "1C":
        shr(evm)
    elif hex_insn == "1D":
        sar(evm)
    elif hex_insn == "20":
        sha3(evm)
    elif hex_insn == "30":
        address(evm)
    elif hex_insn == "31":
        balance(evm)
    elif hex_insn == "32":
        origin(evm)
    elif hex_insn == "33":
        caller(evm)
    elif hex_insn == "34":
        callvalue(evm)
    elif hex_insn == "35":
        calldataload(evm)
    elif hex_insn == "36":
        calldatasize(evm)
    elif hex_insn == "37":
        calldatacopy(evm)
    elif hex_insn == "38":
        codesize(evm)
    elif hex_insn == "39":
        codecopy(evm)
    elif hex_insn == "3A":
        gasprice(evm)
    elif hex_insn == "3B":
        extcodesize(evm)
    elif hex_insn == "3C":
        extcodesize(evm)
    elif hex_insn == "3D":
        returndatasize(evm)
    elif hex_insn == "3E":
        returndatacopy(evm)
    elif hex_insn == "3F":
        extcodehash(evm)
    elif hex_insn == "40":
        blockhash(evm)
    elif hex_insn == "41":
        coinbase(evm)
    elif hex_insn == "42":
        timestamp(evm)
    elif hex_insn == "43":
        number(evm)
    elif hex_insn == "44":
        difficulty(evm)
    elif hex_insn == "45":
        gaslimit(evm)
    elif hex_insn == "46":
        chainid(evm)
    elif hex_insn == "47":
        selfbalance(evm)
    elif hex_insn == "48":
        basefee(evm)
    elif hex_insn == "50":
        pop(evm)
    elif hex_insn == "51":
        mload(evm)
    elif hex_insn == "52":
        mstore(evm)
    elif hex_insn == "53":
        mstore8(evm)
    elif hex_insn == "54":
        sload(evm)
    elif hex_insn == "55":
        sstore(evm)
    elif hex_insn == "56":
        jump(evm)
    elif hex_insn == "57":
        jumpi(evm)
    elif hex_insn == "58":
        pc(evm)
    elif hex_insn == "59":
        msize(evm)
    elif hex_insn == "5A":
        gas(evm)
    elif hex_insn == "5B":
        jumpdest(evm)
    elif readable_insn[:4] == "PUSH":
        push(evm, insn.get_metadata())
    elif readable_insn[:3] == "DUP":
        dup(evm, insn.get_metadata())
    elif readable_insn[:4] == "SWAP":
        swap(evm, insn.get_metadata())
    elif hex_insn == "A0":
        log0(evm)
    elif hex_insn == "A1":
        log1(evm)
    elif hex_insn == "A2":
        log2(evm)
    elif hex_insn == "A3":
        log3(evm)
    elif hex_insn == "A4":
        log4(evm)
    elif hex_insn == "F0":
        create(evm)
    elif hex_insn == "F1":
        call(evm)
    elif hex_insn == "F2":
        callcode(evm) 
    elif hex_insn == "F3":
        return_op(evm)
    elif hex_insn == "F4":
        delegatecall(evm)
    elif hex_insn == "F5":
        create2(evm)
    elif hex_insn == "FA":
        staticcall(evm)
    elif hex_insn == "FD":
        revert(evm)
    elif hex_insn == "FF":
        selfdestruct(evm)
    else:
        # Might have to incorporate for INVALID
        raise EVMInstructionNotFound(hex_insn)
    
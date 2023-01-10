"""
Module containing the logic for all EVM operations

Each function takes care of the associated stack, memory, program counter, and
gas 
"""

from evm import EVM, EVMInstruction
from u256 import U256
from gas import charge_gas, sstore_gas_check
from hashing import keccak256
from exceptions import *
from data import EVMMemoryReturnValue
from utils.address import EVMAddress
from ..logs import EVMLog

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

    # Every two chars is a byte
    value_byte_len = len(value.get_value()) // 2
    value_word_len = (value_byte_len + 31) // 32 

    hashed_value = keccak256(hex = value)

    evm._stack.push(
        U256(int(hashed_value, 16))
    )

    evm._pc += 1

    charge_gas(
        evm, 
        "20", 
        {
            "data_size_words": value_word_len,
            "mem_expansion_cost": value.get_mem_expansion_cost()
        }
    )

def address(evm: EVM):

    evm._stack.push(
        evm._msg.get_recipient()
    )

    evm._pc += 1

    charge_gas(evm, "30")

def balance(evm: EVM):

    address = evm._stack.pop()

    is_touched = evm._storage.is_address_touched(EVMAddress(uint=address))

    evm._stack.push(
        evm._storage.get_contract_balance(EVMAddress(uint=address))
    )

    evm._pc += 1

    charge_gas(evm, "31", is_touched)

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

    destOffset = evm._stack.pop()
    offset = evm._stack.pop()
    length = evm._stack.pop()
    
    data = evm._msg.load_data_custom(offset, length)

    return_value = evm._memory.store_custom(destOffset, length, data)

    words = (length.to_int() + 31) // 32

    evm._pc += 1

    charge_gas(
        evm, 
        "37",
        {
            words,
            return_value.get_mem_expansion_cost()
        }
        )

def codesize(evm: EVM):

    evm._stack.push(
        evm._rom.get_size()
    )

    evm._pc += 1

    charge_gas(evm, "38")

def codecopy(evm: EVM):
    
    destOffset = evm._stack.pop()
    offset = evm._stack.pop()
    length = evm._stack.pop()

    code = evm._rom.get_code(offset, length)

    return_val = evm._memory.store_custom(destOffset, length, code)

    words = (length.to_int() + 31) // 32

    evm._pc += 1

    charge_gas(
        evm,
        "39",
        {
            "data_size_words": words,
            "mem_expansion_cost": return_val.get_mem_expansion_cost()
        }
    )

def gasprice(evm: EVM):

    evm._stack.push(
        evm._tx.get_gas_price()
    )

    evm._pc += 1

    charge_gas(evm, "3A")

def extcodesize(evm: EVM):

    address = EVMAddress(evm._stack.pop())

    is_touched = evm._storage.is_address_touched(address)

    size = evm._storage.get_contract_bytecode_size(address)

    evm._stack.push(size)

    evm._pc += 1

    charge_gas(evm, "3B", is_touched)


def extcodecopy(evm: EVM):

    address = EVMAddress(evm._stack.pop())
    destOffset = evm._stack.pop()
    offset = evm._stack.pop()
    length = evm._stack.pop()

    is_touched = evm._storage.is_address_touched(address)

    code = evm._storage.get_contract_bytecode_custom(address, offset, length)

    code_len = len(code) // 2 # Bytes
    data_size_words = (code_len + 31) // 32

    return_val = evm._memory.store_custom(destOffset, length, code)

    evm._pc += 1

    charge_gas(
        evm, 
        "3C", 
        {
            "is_touched": is_touched,
            "data_size_words": data_size_words,
            "mem_expansion_cost": return_val.get_mem_expansion_cost()
        }
    )

def returndatasize(evm: EVM):

    evm._stack.push(
        U256(len(evm._return_data.get_data()))
    )

    evm._pc += 1

    charge_gas(evm, "3D")

def returndatacopy(evm: EVM):

    destOffset = evm._stack.pop()
    offset = evm._stack.pop()
    length = evm._stack.pop()

    data = evm._return_data.get_data_custom(offset, length)

    data_size = len(data) // 2
    data_word_size = (data_size + 31) // 32

    return_val = evm._memory.store_custom(destOffset, length, data)

    evm._pc += 1

    charge_gas(
        evm, 
        "3E", 
        {
            "data_size_words": data_word_size,
            "mem_expansion_cost": return_val.get_mem_expansion_cost()
        }
        )

def extcodehash(evm: EVM):

    pass

def blockhash(evm: EVM):

    pass

def coinbase(evm: EVM):

    evm._stack.push(
        evm._current_block.get_coinbase()
    )

    evm._pc += 1

    charge_gas(evm, "41")

def timestamp(evm: EVM):

    evm._stack.push(
        evm._current_block.get_timestamp()
    )

    evm._pc += 1

    charge_gas(evm, "42")

def number(evm: EVM):

    evm._stack.push(
        evm._current_block.get_number()
    )

    evm._pc += 1

    charge_gas(evm, "43")

def difficulty(evm: EVM):

    evm._stack.push(
        evm._current_block.get_difficulty()
    )

    evm._pc += 1

    charge_gas(evm, "44")

def gaslimit(evm: EVM):

    evm._stack.push(
        evm._current_block.get_gas_limit()
    )

    evm._pc += 1

    charge_gas(evm, "45")

def chainid(evm: EVM):

    evm._stack.push(
        U256(evm._state.get_chain_id())
    )

    evm._pc += 1

    charge_gas(evm, "46")

def selfbalance(evm: EVM):

    # Don't need to check for touched addresses since executing contract's
    # addresses is already added during EVM initialization

    evm._stack.push(
        evm._storage.get_contract_balance(evm._msg.get_recipient())
    )

    evm._pc += 1

    charge_gas(evm, "47")

def basefee(evm: EVM):

    evm._stack.push(
        evm._current_block.get_base_fee()
    )

    evm._pc += 1

    charge_gas(evm, "48")

def pop(evm: EVM):

    evm._stack.pop()

    evm._pc += 1

    charge_gas(evm, "50")

def mload(evm: EVM):

    offset = evm._stack.pop()

    return_val = evm._memory.load(offset)

    evm._pc += 1

    charge_gas(evm, "51", return_val.get_mem_expansion_cost())

def mstore(evm: EVM):

    offset = evm._stack.pop()
    value = evm._stack.pop()

    return_val = evm._memory.store(offset, value)

    evm._pc += 1

    charge_gas(evm, "52", return_val.get_mem_expansion_cost())

def mstore8(evm: EVM):

    offset = evm._stack.pop()
    value = evm._stack.pop()

    value = U256.bitwise_and(value, U256(255))

    return_val = evm._memory.store(offset, value)

    evm._pc += 1

    charge_gas(evm, "53", return_val.get_mem_expansion_cost())

def sload(evm: EVM):

    key = evm._stack.pop()

    is_slot_touched = evm._storage.is_storage_slot_touched(evm._msg.get_recipient())

    value = evm._storage.load(
        evm._msg.get_recipient(),
        key
    )

    evm._stack.push(value)

    evm._pc += 1

    charge_gas(evm, "54", is_slot_touched)

def sstore(evm: EVM):
    """
    Perhaps the most difficult operation in terms of gas...
    """
    key = evm._stack.pop()
    new_value = evm._stack.pop()

    original_value = evm._storage.load_immutable(
        evm._msg.get_recipient(),
        key
    )
    current_value = evm._storage.load(
        evm._msg.get_recipient(),
        key
    )

    gas_cost = 0
    gas_refund = 0

    sstore_gas_check(evm)

    is_slot_touched = evm._storage.is_storage_slot_touched(
        evm._msg.get_recipient(),
        key
    )

    if not is_slot_touched:

        gas_cost += 2100

    if new_value.to_int() == current_value.to_int():
        gas_cost += 100
    else: # new_value != current_value
        if current_value.to_int() == original_value.to_int():
            if original_value.to_int() == 0:
                gas_cost += 20000
            else: # original_value != 0
                gas_cost += 2900
                if new_value.to_int() == 0:
                    gas_refund += 4800
        else: # current_value != original value
            gas_cost += 100
            if original_value.to_int() != 0:
                if current_value.to_int() == 0:
                    gas_refund -= 4800
                elif new_value.to_int() == 0:
                    gas_refund += 4800
            if new_value.to_int() == original_value.to_int():
                if original_value.to_int() == 0:
                    gas_refund += 19900
                else: # original_value != 0
                    gas_refund += 2800

    evm._storage.store(
        evm._msg.get_recipient(),
        key, 
        new_value
    )

    evm._pc += 1

    charge_gas(
        evm, 
        "55", 
        {
            "gas_cost": gas_cost,
            "gas_refund": gas_refund,
            "is_touched": is_slot_touched
        }
        )

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
        U256(evm._pc)
    )

    evm._pc += 1

    charge_gas(evm, "58")

def msize(evm: EVM):

    evm._stack.push(
        evm._memory.get_size()
    )

    evm._pc += 1

    charge_gas(evm, "59")

def gas(evm: EVM):

    evm._stack.push(
        U256(evm._gas)
    )

    evm._pc += 1

    charge_gas(evm, "5A")

def jumpdest(evm: EVM):

    evm._pc += 1
    charge_gas(evm, "5B")

def push(evm: EVM, bytes_to_push: int):

    evm._stack.push(
        U256(bytes_to_push)
    )

    evm._pc += 1

    charge_gas(evm, "PUSH")

def dup(evm: EVM, index_to_dup: int):

    dup_value = evm._stack.get_item(U256(index_to_dup))

    evm._stack.push(
        dup_value
    )

    evm._pc += 1

    charge_gas(evm, "DUP")

def swap(evm: EVM, index_to_swap: int):

    b = evm._stack.get_item(U256(index_to_swap))
    a = evm._stack.pop()
    
    evm._stack.push(b)
    evm._stack.insert(U256(index_to_swap), a)

    evm._pc += 1

    charge_gas(evm, "SWAP")

def log0(evm: EVM):

    offset = evm._stack.pop()
    length = evm._stack.pop()

    return_val = evm._memory.load_custom(offset, length)

    log = EVMLog(
        evm._msg.get_recipient(),
        return_val.get_value()
    )

    evm._log_storage.add_log(log)

    evm._pc += 1

    charge_gas(evm , "A0", return_val.get_mem_expansion_cost())

def log1(evm: EVM):

    offset = evm._stack.pop()
    length = evm._stack.pop()
    topic0 = evm._stack.pop()

    return_val = evm._memory.load_custom(offset, length)

    log = EVMLog(
        evm._msg.get_recipient(),
        return_val.get_value(),
        topic0=topic0.to_hex_string()
        )

    evm._log_storage.add_log(log)

    evm._pc += 1

    charge_gas(evm , "A0", return_val.get_mem_expansion_cost())

def log2(evm: EVM):

    offset = evm._stack.pop()
    length = evm._stack.pop()
    topic0 = evm._stack.pop()
    topic1 = evm._stack.pop()

    return_val = evm._memory.load_custom(offset, length)

    log = EVMLog(
        evm._msg.get_recipient(),
        return_val.get_value(),
        topic0=topic0.to_hex_string(),
        topic1=topic1.to_hex_string()
        )

    evm._log_storage.add_log(log)

    evm._pc += 1

    charge_gas(evm , "A0", return_val.get_mem_expansion_cost())

def log3(evm: EVM):

    offset = evm._stack.pop()
    length = evm._stack.pop()
    topic0 = evm._stack.pop()
    topic1 = evm._stack.pop()
    topic2 = evm._stack.pop()

    return_val = evm._memory.load_custom(offset, length)

    log = EVMLog(
        evm._msg.get_recipient(),
        return_val.get_value(),
        topic0=topic0.to_hex_string(),
        topic1=topic1.to_hex_string(),
        topic2=topic2.to_hex_string()
        )

    evm._log_storage.add_log(log)

    evm._pc += 1

    charge_gas(evm , "A0", return_val.get_mem_expansion_cost())

def log4(evm: EVM):

    offset = evm._stack.pop()
    length = evm._stack.pop()
    topic0 = evm._stack.pop()
    topic1 = evm._stack.pop()
    topic2 = evm._stack.pop()
    topic3 = evm._stack.pop()

    return_val = evm._memory.load_custom(offset, length)

    log = EVMLog(
        evm._msg.get_recipient(),
        return_val.get_value(),
        topic0=topic0.to_hex_string(),
        topic1=topic1.to_hex_string(),
        topic2=topic2.to_hex_string(),
        topic3=topic3.to_hex_string()
        )

    evm._log_storage.add_log(log)

    evm._pc += 1

    charge_gas(evm , "A0", return_val.get_mem_expansion_cost())

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
    
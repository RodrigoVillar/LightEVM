
from .exceptions import *
from ..evm import EVM

def sstore_gas_check(evm: EVM):

    if evm._gas <= 2300:

        raise EVMInsufficientGas()

def charge_gas(evm: EVM, insn: str, metadata = None) -> int:
    """
    insn must be a string representing the hexadecimal represenation of the
    instruction gas is being charged for

    If charging for EXP operation, metadata is the number of bits of the
    exponent
    
    If charging for SHA3 operation, metadata is a dictionary with the following
    keys: data_size_words, mem_expansion_cost
    
    If charging for CALLDATA, CODECOPY, or RETURNDATACOPY operation, then metadata is a dictionary with the following
    keys: data_size_words, mem_expansion_cost

    If charging for BALANCE, EXTCODESIZE, or EXTCODEHASH, then metadata is a
    boolean representing whether if the address was touched or not

    If charging for EXTCODECOPY, then metadata is a dict with the following
    keys: is_touched, data_size_words, mem_expansion_cost

    If charging for SSTORE operation, then metadata is a dict with the following
    keys: gas_cost, gas_refund, is_touched

    If charging for SLOAD operation, then metadata is a boolean representing
    whether the storage slot was touched or not
    """

    insn = insn.upper()

    # If instruction has static gas cost
    if insn in opcodes_gas:

        if evm._gas - opcodes_gas[insn] < 0:

            raise EVMInsufficientGas()

        evm._gas -= opcodes_gas[insn]

        return

    # Branch between all dynamic opcodes

    if insn == "0A": # EXP OPERATION
        exp_bytes = (metadata + 7) // 8
        gas_cost = 10 + (50 * exp_bytes)
        if evm._gas - gas_cost < 0:

            raise EVMInsufficientGas()

        evm._gas -= gas_cost

    elif insn == "20": # SHA3 OPERATION

        gas_cost = 30 + 6 * metadata["data_size_words"] + metadata["mem_expansion_cost"]

        if evm._gas - gas_cost < 0:

            raise EVMInsufficientGas()

        evm._gas -= gas_cost

    elif insn == "37": # CALLDATACOPY

        gas_cost = 3 + (3 * metadata["data_size_words"]) + metadata["mem_expansion_cost"]

        if evm._gas - gas_cost < 0:

            raise EVMInsufficientGas()

        evm._gas -= gas_cost

    elif insn == "39": # CODECOPY

        pass

    elif insn == "3C": # EXTCODECOPY

        pass

    elif insn == "55": # SSTORE

        pass

    elif insn == "PUSH":

        if evm._gas - 3 < 0:

            raise EVMInsufficientGas()

        evm._gas -= 3

    elif insn == "DUP":

        pass
    else:
        raise EVMNoAssociatedGasCost(insn)

# The following opcodes have dynamic gas prices
# EXP, SHA3, CALLDATACOPY, CODECOPY, EXTCODECOPY, SSTORE, LOG0, LOG1, LOG2,
# LOG3, LOG4. CALL, CALLCODE, DELEGATECALL, SELFDESTRUCT
opcodes_gas = {
"00" : 		0,
"01" : 		3,
"02" : 		5,
"03" : 		3,
"04" : 		5,
"05" : 		5,
"06" : 		5,
"07" : 		5,
"08" : 		8,
"09" : 		8,
"0B" : 		5,
"10" : 		3,
"11" : 		3,
"12" : 		3,
"13" : 		3,
"14" : 		3,
"15" : 		3,
"16" : 		3,
"17" : 		3,
"18" : 		3,
"19" : 		3,
"1A" : 		3,
"30" : 		2,
"31" : 		400,
"32" : 		2,
"33" : 		2,
"34" : 		2,
"35" : 		3,
"36" : 		2,
"38" : 		2,
"3A" : 		2,
"3B" : 		700,
"40" : 		20,
"41" : 		2,
"42" : 		2,
"43" : 		2,
"44" : 		2,
"45" : 		2,
"50" : 		2,
"51" : 		3,
"52" : 		3,
"53" : 		3,
"54" :  	200,
"56" : 		8,
"57" : 		10,
"58" : 		2,
"59" : 		2,
"5A" : 		2,
"5B" : 		1,
"60" : 3,  
"61" : 3, 
"62" : 3, 
"63" : 3, 
"64" : 3, 
"65" : 3, 
"66" : 3, 
"67" : 3, 
"68" : 3, 
"69" : 3, 
"6A" : 3, 
"6B" : 3, 
"6C" : 3, 
"6D" : 3, 
"6E" : 3, 
"6F" : 3, 
"70" : 3, 
"71" : 3, 
"72" : 3, 
"73" : 3, 
"74" : 3, 
"75" : 3, 
"76" : 3, 
"77" : 3, 
"78" : 3, 
"79" : 3, 
"7A" : 3, 
"7B" : 3, 
"7C" : 3, 
"7D" : 3, 
"7E" : 3, 
"7F" : 3, 
"80" : 3, 
"81" : 3, 
"82" : 3, 
"83" : 3, 
"84" : 3, 
"85" : 3, 
"86" : 3, 
"87" : 3, 
"88" : 3, 
"89" : 3, 
"8A" : 3, 
"8B" : 3, 
"8C" : 3, 
"8D" : 3, 
"8E" : 3, 
"8F" : 3, 
"90" : 3, 
"91" : 3, 
"92" : 3, 
"93" : 3, 
"94" : 3, 
"95" : 3, 
"96" : 3, 
"97" : 3, 
"98" : 3, 
"99" : 3, 
"9A" : 3, 
"9B" : 3, 
"9C" : 3, 
"9D" : 3, 
"9E" : 3, 
"9F" : 3, 
"F0" : 32000,
"F3" : 0
}
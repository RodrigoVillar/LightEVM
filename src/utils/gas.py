
from utils.exceptions import *
from evm import EVM


def charge_gas(evm: EVM, insn: str, metadata = None) -> int:
    """
    insn must be a string representing the hexadecimal represenation of the
    instruction gas is being charged for

    If charging for EXP operation, metadata is the number of bits of the
    exponent
    
    If charging for SHA3 operation, metadata is the word size of the value being hashed 
    """

    insn = insn.upper()

    # If instruction has static gas cost
    if insn in opcodes_gas:

        if evm._gas - opcodes_gas[insn] < 0:

            raise EVMInsufficientGas()

        evm._gas -= opcodes_gas[insn]

    # If instruction is valid
    if insn in opcodes_str:

        # Branch between all dynamic opcodes

        if insn == "0A": # EXP OPERATION
            exp_bytes = (metadata + 7) // 8
            gas_cost = 10 + (50 * exp_bytes)
            if evm._gas - gas_cost < 0:

                raise EVMInsufficientGas()

            evm._gas -= gas_cost

        elif insn == "20": # SHA3 OPERATION

            gas_cost = 30 + (6 * metadata)
            
            if evm._gas - gas_cost < 0:

                raise EVMInsufficientGas()

            evm._gas -= gas_cost

        elif insn == "37": # CALLDATACOPY

            pass

        elif insn == "39": # CODECOPY

            pass

        elif insn == "3C": # EXTCODECOPY

            pass

        elif insn == "55": # SSTORE

            pass

    raise EVMNoAssociatedGasCost(insn)

opcodes_str = {
"00"      : "STOP",
"01"      : "ADD",
"02"      : "MUL",
"03"      : "SUB",
"04"      : "DIV",
"05"      : "SDIV",
"06"      : "MOD",
"07"      : "SMOD",
"08"      : "ADDMOD",
"09"      : "MULMOD",
"0A"      : "EXP",
"0B"      : "SIGNEXTEND",
"10"      : "LT",
"11"      : "GT",
"12"      : "SLT",
"13"      : "SGT",
"14"      : "EQ",
"15"      : "ISZERO",
"16"      : "AND",
"17"      : "OR",
"18"      : "XOR",
"19"      : "NOT",
"1A"      : "BYTE",
"1B"      : "SHL",
"1C"      : "SHR",
"1D"      : "SAR",
"20"      : "SHA3",
"30"      : "ADDRESS",
"31"      : "BALANCE",
"32"      : "ORIGIN",
"33"      : "CALLER",
"34"      : "CALLVALUE",
"35"      : "CALLDATALOAD",
"36"      : "CALLDATASIZE",
"37"      : "CALLDATACOPY",
"38"      : "CODESIZE",
"39"      : "CODECOPY",
"3A"      : "GASPRICE",
"3B"      : "EXTCODESIZE",
"3C"      : "EXTCODECOPY",
"3D"      : "RETURNDATASIZE",
"3E"      : "RETURNDATACOPY",
"3F"      : "EXTCODEHASH",
"40"      : "BLOCKHASH",
"41"      : "COINBASE",
"42"      : "TIMESTAMP",
"43"      : "NUMBER",
"44"      : "DIFFICULTY",
"45"      : "GASLIMIT",
"46"      : "CHAINID",
"47"      : "SELFBALANCE",
"48"      : "BASEFEE",
"50"      : "POP",
"51"      : "MLOAD",
"52"      : "MSTORE",
"53"      : "MSTORE8",
"54"      : "SLOAD",
"55"      : "SSTORE",
"56"      : "JUMP",
"57"      : "JUMPI",
"58"      : "PC",
"59"      : "MSIZE",
"5A"      : "GAS",
"5B"      : "JUMPDEST",
"60"      : "PUSH1",
"61"      : "PUSH2",
"62"      : "PUSH3",
"63"      : "PUSH4",
"64"      : "PUSH5",
"65"      : "PUSH6",
"66"      : "PUSH7",
"67"      : "PUSH8",
"68"      : "PUSH9",
"69"      : "PUSH10",
"6A"      : "PUSH11",
"6B"      : "PUSH12",
"6C"      : "PUSH13",
"6D"      : "PUSH14",
"6E"      : "PUSH15",
"6F"      : "PUSH16",
"70"      : "PUSH17",
"71"      : "PUSH18",
"72"      : "PUSH19",
"73"      : "PUSH20",
"74"      : "PUSH21",
"75"      : "PUSH22",
"76"      : "PUSH23",
"77"      : "PUSH24",
"78"      : "PUSH25",
"79"      : "PUSH26",
"7A"      : "PUSH27",
"7B"      : "PUSH28",
"7C"      : "PUSH29",
"7D"      : "PUSH30",
"7E"      : "PUSH31",
"7F"      : "PUSH32",
"80"      : "DUP1",
"81"      : "DUP2",
"82"      : "DUP3",
"83"      : "DUP4",
"84"      : "DUP5",
"85"      : "DUP6",
"86"      : "DUP7",
"87"      : "DUP8",
"88"      : "DUP9",
"89"      : "DUP10",
"8A"      : "DUP11",
"8B"      : "DUP12",
"8C"      : "DUP13",
"8D"      : "DUP14",
"8E"      : "DUP15",
"8F"      : "DUP16",
"90"      : "SWAP1",
"91"      : "SWAP2",
"92"      : "SWAP3",
"93"      : "SWAP4",
"94"      : "SWAP5",
"95"      : "SWAP6",
"96"      : "SWAP7",
"97"      : "SWAP8",
"98"      : "SWAP9",
"99"      : "SWAP10",
"9A"      : "SWAP11",
"9B"      : "SWAP12",
"9C"      : "SWAP13",
"9D"      : "SWAP14",
"9E"      : "SWAP15",
"9F"      : "SWAP16",
"A0"      : "LOG0",
"A1"      : "LOG1",
"A2"      : "LOG2",
"A3"      : "LOG3",
"A4"      : "LOG4",
"F0"      : "CREATE",
"F1"      : "CALL",
"F2"      : "CALLCODE",
"F3"      : "RETURN",
"F4"      : "DELEGATECALL",
"F5"      : "CREATE2",
"FA"      : "STATICCALL",
"FD"      : "REVERT",
"FF"      : "SELFDESTRUCT",
}

push_opcodes = [
    "60",
    "61",
    "62",
    "63",
    "64",
    "65",
    "66",
    "67",
    "68",
    "69",
    "6A",
    "6B",
    "6C",
    "6D",
    "6E",
    "6F",
    "70",
    "71",
    "72",
    "73",
    "74",
    "75",
    "76",
    "77",
    "78",
    "79",
    "7A",
    "7B",
    "7C",
    "7D",
    "7E",
    "7F"
]

dup_opcodes = [
    "81",
    "82",
    "83",
    "84",
    "85",
    "86",
    "87",
    "88",
    "89",
    "8A",
    "8B",
    "8C",
    "8D",
    "8E",
    "8F"
]

swap_opcodes = [
    "91",
    "92",
    "93",
    "94",
    "95",
    "96",
    "97",
    "98",
    "99",
    "9A",
    "9B",
    "9C",
    "9D",
    "9E",
    "9F"
]

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
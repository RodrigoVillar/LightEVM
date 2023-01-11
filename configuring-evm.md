# Setting Up `execution.toml`

LightEVM uses `execution.toml` to set all values necessary to initialize an
instance of the EVM.

The execution file contains the following sections:

-   [Chain](#chain)
-   [Block](#block)
-   [Transaction](#transaction)
-   [Contracts](#contracts)

## Chain

The `[chain]` section is a necessary section which contains values relevant to the EVM chain being used to
simulate the transaction

### chain_id

Required: True

Integer representing the ID of the chain being utilized. For example, if simulating on the Ethereum blockchain, set chain_id = 1

## Block

### timestamp

Required: True

Integer representing the block current in UNIX

### difficulty

Required: True

Integer representing the difficulty of the block

### gas_limit

Required: True

Integer representing the maximum amount of gas to be used in the transaction

### base_fee

Required: true

Integer (denominated in Wei) representing the base fee of any transaction in the block

### number

Required: true

Integer representing the block number

### coinbase

Required: true

Hexadecimal string representing the address of the node which appended the block
to the blockchain

## Transaction

The `[transaction]` section is a necesssary section which contains all values
relevant to the transaction being simulated

### from

Required: True

Hexadecimal string representing the address of the transaction sender

### to

Required: True

Hexadecimal string representing the address of the transaction recipient

### calldata

Required: False

Hexadecimal string representing the data passed with the transaction

### value

Required: true

Integer (denominated in Wei) representing the amount of ether passed with the
transaction

### gas_limit

Required: True

Integer representing the maximum amount of gas to be used in the transaction

### is_transfer_only

Required: True

Boolean representing whether the transaction is a simple eth transfer

### type

Required: True

Integer representing the type of the transaction

### sig

Required: only if calldata is utilized

Hexadecimal string representing the function signature of the transaction
If the transaction calls a contract, then the function signature is the first
four bytes of the transaction calldata

## Contracts

The `[contracts]` section is an optional array section which contains all contract
data to be imported

### address

Required: True

Hexadecimal string representing the address of the particular contract

### bytecode

Required: True

Hexadecimal string representing the bytecode of the particular contract

### balance

Required: True

Integer representing the balance of the particular contract (denominated in Wei)

### Nonce

Required: True

Integer representing the nonce of the particular contract

### slots

Required: True

Section of integer-integer key pairs representing the storage slots of the
particular contract

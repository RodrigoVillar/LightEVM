# LightEVM

Basic implementation of the Ethereum Virtual Machine written in Python

LightEVM is aimed for advanced Ethereum users who wish to simulate transactions
on Ethereum, but do not want to go through the hassle of setting up a node and
writing a custom script to feed in their transaction

## Getting Set Up

-   LightEVM requires Python v3.9.13
-   Create a virtual environment using: `python -m venv venv`
-   Run `source venv/bin/activate` to set your environment to that of the
    virtual environment
-   Run `pip install -r requirements.txt` to install all necessary dependencies

## Running LightEVM

Once setting up both the execution environment and `execution.toml`, run
`python main.py` inside the source folder

## Simulating Transactions

For information regarding the semantics of `execution.toml`, please refer to the
[manual](./configuring-evm.md) on setting up the EVM

## Notes

-   LightEVM does not support any transaction whose logic results in any CALL
    opcode being called, as support for multiple instances of the EVM is not yet
    supported
-   Furthermore, LightEVM does not support any transactions that result in the
    creation of new contracts

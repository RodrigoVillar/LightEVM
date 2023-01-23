# LightEVM

Basic implementation of the Ethereum Virtual Machine written in Python

LightEVM is aimed for advanced Ethereum users who wish to simulate transactions
on Ethereum, but do not want to go through the hassle of setting up a node and
writing a custom script to feed in their transaction

## Getting Set Up

-   LightEVM requires Python v3.9.13
-   Create a virtual environment via the following:

```bash
python -m venv venv
```

-   To activate the virtual envuronment and install all dependencies, do the
    following:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Running LightEVM

After activating the virtual environment, run the following to start an instance
of LightEVM:

```
python main.py
```

## Connecting to a Node

By default, LightEVM utilizes all information passed in by the user in
[`execution.toml`](./execution.toml) to create an instance of LightEVM. For
variables such as the current block number or the transaction gas limit,
LightEVM will be able to retrieve these values as otherwise, this would imply
that the user never passed in such values in the first place.

The one area where there this does not apply is for contract data. In the case
where LightEVM needs to interact with a contract whose data is not stored
locally (i.e. not passed in by the user), LightEVM will attempt to make a call
to the API URL designated in `.env` to grab the desired information. If the user
does not provide an API URL and contract data needs to be grabbed externally,
LightEVM will revert.

All logic that relate to the usage of `API_URL` can be found in [`state.py`](./src/state.py)

### Setting Up .env File

-   Using `template.env` as a base template, set `API_KEY` equal to the url of an
    RPC node. Then rename `template.env` to `.env` so LightEVM can use said RPC
    node to pull necessary contract data whenever it is not stored locally
-   Your `.env` file should look like the following:

```env
API_URL="<INSERT API URL HERE>"
```

## Simulating Transactions

For information regarding the semantics of [`execution.toml`](./execution.toml), please refer to the
[manual](./configuring-evm.md) on setting up the EVM

## Notes

-   LightEVM does not support any transaction whose logic results in any CALL
    opcode being called, as support for multiple instances of the EVM is not yet
    supported
-   Furthermore, LightEVM does not support any transactions that result in the
    creation of new contracts

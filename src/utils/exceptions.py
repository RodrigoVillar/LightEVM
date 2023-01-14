"""
File containing all util-related exceptions
"""

class U256InputOutOfBounds(Exception):

    pass

class U256InvalidInputType(Exception):

    pass

class S256InvalidType(Exception):

    pass

class EVMInsufficientGas(Exception):

    pass

class EVMNoAssociatedGasCost(Exception):

    pass

class EVMInstructionNotFound(Exception):

    pass

class EVMInvalidJumpDesination(Exception):

    pass

class EVMUnkwownAccountType(Exception):

    pass

class EVMStackOverFlow(Exception):

    pass

class EVMOutsideStackBounds(Exception):

    pass

class EVMUndefinedStackItem(Exception):

    pass

class U256AddressConversionFailure(Exception):

    pass

class EVMStackInvalidInputType(Exception):

    pass

class EVMEmptyStack(Exception):

    pass

class EVMOperationNotImplemented(Exception):

    pass

class EVMStackItemEmpty(Exception):

    pass

class EVMInvalidStackIndex(Exception):

    pass

class EVMInvalidStackDupIndex(Exception):

    pass
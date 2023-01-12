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
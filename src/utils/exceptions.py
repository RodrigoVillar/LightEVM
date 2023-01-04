"""
File containing all util-related exceptions
"""

class U256OutOfBounds(Exception):

    pass

class U256InvalidType(Exception):

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
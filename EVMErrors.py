"""
Module containing all EVM errors
"""

class EVMStackOverFlow(Exception):

    pass

class EVMStackItemError(Exception):

    pass

class EVMOutOfGasError(Exception):

    pass

class EVMGasNotImplemented(Exception):

    pass

class EVMStackEmpty(Exception):

    pass

class EVMOperationNotImplemented(Exception):

    pass

class EVMInvalidJumpDestination(Exception):

    pass

class EVMOutsideStackBounds(Exception):

    pass

class EVMUndefinedStackItem(Exception):

    pass
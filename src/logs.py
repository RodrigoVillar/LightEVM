"""
Module containing the EVMLog class
"""
from utils.address import EVMAddress

class EVMLog:
    """
    Class representing Ethereum Logs
    """
    
    def __init__(self, address: EVMAddress, data: str, topic0: str = None, topic1: str = None, topic2: str = None, topic3: str = None):

        self._address = address
        self._data = data
        self._topic0 = topic0
        self._topic1 = topic1
        self._topic2 = topic2
        self._topic3 = topic3

class EVMLogStorage:
    """
    Class responsible for storing EVMLog objects across multiple execution contexts
    """
    def __init__(self):

        self._logs = []

    def add_log(self, log: EVMLog):

        self._logs.append(log)
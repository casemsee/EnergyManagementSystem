"""
Middle term operation classes for universal ems, local ems and stand alone ems
@author: Tianyang Zhao
@date: 24 Jan 2018
@email: zhaoty@ntu.edu.sg
"""

from utils import Logger
from long_term_operation.main import long_term_operation

class LongTermOperation():
    """
    Stand alone short term operation process
    """
    def __init__(self):
        self.logger = Logger("Long_term_operation_ems")

    def run(self, micorgird, session):
        long_term_operation(micorgird,session,self.logger)
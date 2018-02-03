"""
Short term operation classes for universal ems, local ems and stand alone ems
@author: Tianyang Zhao
@date: 23 Jan 2018
@email: zhaoty@ntu.edu.sg
"""

from utils import Logger
from short_term_operation.main import short_term_operation


class ShortTermOperation():
    """
    Stand alone short term operation process
    """

    def __init__(self):
        self.logger = Logger("Short_term_operation_ems")

    def run(self, micorgird, session, session_history):
        short_term_operation(micorgird, session, session_history, self.logger)

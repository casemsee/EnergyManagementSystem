"""
Middle term operation classes for universal ems, local ems and stand alone ems
@author: Tianyang Zhao
@date: 23 Jan 2018
@email: zhaoty@ntu.edu.sg
"""

from utils import Logger
from middle_term_operation.main import middle_term_operation

class MiddleTermOperation():
	"""
	Stand alone short term operation process
	"""
	def __init__(self):
		self.logger = Logger("Middle_term_operation_ems")

	def run(self, micorgird, session, session_history):
		middle_term_operation(micorgird,session,session_history,self.logger)

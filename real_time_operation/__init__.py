"""
Two functions are provided in this module
1) Real time controller
2) Resource manager
"""
from utils import  Logger

class RealTimeSimulation():
	"""
	Real time simulation class for one microgrid
	The calculation method is the same within the function of real time balancing(RTB/AGC)
	It should be noted that, other calculation method can be applied as well.
	"""
	def __init__(self):
		self.name = "Real time operation"
		self.priority = 100
		self.logger = Logger("Real time simulation")
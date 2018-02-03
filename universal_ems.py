## Main entrance for the universal energy management (UEMS).
# Documentation for the local EMS.
# \author: Tianyang Zhao
# \mail: zhaoty@ntu.edu.sg
# \date: 22/Jan/2018
#

# The following packages are required to deploy UEMS
# 1) Python 3.6+
# 2) MySQL
# 3) Zeromq
# 4) APScheduler
# 5) Gurobi*(academic use only)
# 6) Mosek*(academic use only)
# 7）Protocol buffer > 3.4.0. The early version does not have the value attribute

from apscheduler.schedulers.blocking import BlockingScheduler  # Scheduler is based on APS
from utils import Logger  # The utility function import from LongQi' work
from modelling.information import single_period_information_pb2  # The information model of economic dispatch
from modelling.information import dynamic_information_pb2
import zmq  # The information channel
# from unit_commitment.main import long_term_operation  # long term operation
# from economic_dispatch.main import middle_term_operation  # middle term operation
from short_term_operation.main import short_term_operation_uems,short_term_operation_lems  # short term operation
from start_up import start_up_lems,start_up_uems
from modelling.information import static_information_pb2 as static_info
from configuration.configuration_global import default_operation_mode

logger = Logger("UEMS")

class Main():
	## The main process of UEMS
	# Further functions can be integrated into the functions
	def __init__(self, socket):
		"""
		Implement the start-up test for universal energy management system
		:param socket: connection socket between local ems and universal ems
		"""
		from start_up import app
		ems_main = app.StartUpLems(socket)# Start up the local EMS

		self.socket = socket
		self.Operation_mode = ems_main.run()

		microgrid_short = start_up_lems.start_up()
		if self.Operation_mode == default_operation_mode["UEMS"]:
			self.microgrid = ems_main.information_collection(microgrid_short,static_info.microgrid())
			self.universal_microgrid = start_up_uems.start_up(microgrid_short)# If uems operates in isolated mode
		else:
			self.microgrid = microgrid_short # If uems operates in isolated mode

		self.Session = ems_main.database_start_up()

def run():
	"""
	Operation function for universal energy management system
	:return:
	"""
	IP = "*"
	# IP = "10.25.255.84"
	# Start the information connection
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://" + IP + ":5555")

	socket_upload = context.socket(zmq.REP)  # Upload information channel for local EMS
	socket_upload.bind("tcp://" + IP + ":5556")

	socket_upload_ed = context.socket(zmq.REP)  # Upload information channel for local EMS
	socket_upload_ed.bind("tcp://" + IP + ":5557")

	socket_upload_uc = context.socket(zmq.REP)  # Upload information channel for local EMS
	socket_upload_uc.bind("tcp://" + IP + ":5558")

	socket_download = context.socket(zmq.REQ)  # Download information channel for local EMS
	socket_download.bind("tcp://" + IP + ":5559")

	initialize = Main(socket)  # Initialized the information and communication system
	session_short = initialize.Session()
	session_middle = initialize.Session()
	session_long = initialize.Session()

	local_model_short = initialize.microgrid
	# local_model_middle = initialize.local_model_middle
	# local_model_long = initialize.local_model_long
	#
	universal_model_short = initialize.universal_microgrid
	# universal_model_middle = initialize.universal_model_middle
	# universal_model_long = initialize.universal_model_long
	# # Start the input information
	info_ed = dynamic_information_pb2.microgrid()  # Dynamic information for economic dispatch
	info_uc = dynamic_information_pb2.microgrid()  # Dynamic information for unit commitment
	info_opf = single_period_information_pb2.microgrid()  # Optimal power flow modelling
	#
	# # Generate different processes
	# logger.info("The short term process in UEMS starts!")
	# sched_uems = BlockingScheduler()  # The schedulor for the optimal power flow
	# sched_uems.add_job(short_term_operation.short_term_operation_uems, 'cron',
	#                    args=(universal_model_short, local_model_short, socket_upload, socket_download, info_opf,
	#                          session_uems_short), minute='0-59',
	#                    second='1')  # The operation is triggered minutely, this process will start at **:01
	#
	# logger.info("The middle term process in UEMS starts!")
	# sched_uems.add_job(middle_term_operation.middle_term_operation_uems, 'cron',
	#                    args=(universal_model_middle, local_model_middle, socket_upload_ed, socket_download, info_ed,
	#                          session_uems_middle), minute='*/5',
	#                    second='5')  # The operation is triggered every 5 minute
	#
	# logger.info("The long term process in UEMS starts!")
	# sched_uems.add_job(long_term_operation.long_term_operation_uems, 'cron',
	#                    args=(universal_model_long, local_model_long, socket_upload_uc, socket_download, info_uc,
	#                          session_uems_long), minute='*/30',
	#                    second='30')  # The operation is triggered every half an hour
	# sched_uems.start()
	for i in range(10):
	#     long_term_operation.long_term_operation_uems(universal_model_long, local_model_long, socket_upload_uc,
	#                                              socket_download, info_uc,
	#                                              session_uems_long)
	#     middle_term_operation.middle_term_operation_uems(universal_model_middle, local_model_middle, socket_upload_ed,
	#                                                 socket_download, info_ed,session_uems_middle)
		short_term_operation_uems(universal_model_short, local_model_short, socket_upload, socket_download, info_opf, session_short, logger)




if __name__ == "__main__":
	## Start the main process of universal energy management
	run()

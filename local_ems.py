# The main entrance of local energy management system (UEMS)
# Date: 21/Jan/2018
# Authors: Tianyang Zhao
# Mail: zhaoty@ntu.edu.sg
from apscheduler.schedulers.blocking import BlockingScheduler  # Time scheduler
import zmq  # The package for information and communication
from start_up import start_up_lems
from modelling.information import static_information_pb2 as static_info
from copy import deepcopy

from utils import Logger
from configuration.configuration_global import default_operation_mode

logger = Logger("Local_ems")

class Main():
    """
    Main class of local energy management system
    """
    def __init__(self,socket):
        """
        :param socket: The input socket of local ems
        """
        from start_up import app
        self.socket = socket
        # self.logger = Logger("Local_ems_start_up")
        ems_main = app.StartUpLems(socket)
        self.Operation_mode = ems_main.run()
        # database start-up operation
        self.Session = ems_main.database_start_up()
        (self.microgrid,self.microgrid_middle,self.microgrid_long) = start_up_lems.start_up() # Generate local ems models
        # self.logger.info("Database has been started up!")
        # operation mode
        if self.Operation_mode == default_operation_mode["UEMS"]:# Local EMS work as the slave of UEMS.
            self.status = ems_main.information_send(self.microgrid, static_info)

    def local_ems(self):# Local ems
        from real_time_operation.app import RealTimeSimulation
        from short_term_operation.app import ShortTermOperation
        from middle_term_operation.app import MiddleTermOperation
        from long_term_operation.app import LongTermOperation

        # S1: Initialize information models
        microgrid = self.microgrid # Obtain the information model
        microgrid_short = deepcopy(microgrid)
        microgrid_middle = self.microgrid_middle
        microgrid_long = self.microgrid_long

        # S2: Initialize databases
        session = self.Session()
        session_short = self.Session()
        session_middle = self.Session()
        session_long = self.Session()

        # S3: Initialize target functions
        real_time_simulation = RealTimeSimulation()
        short_term_operation = ShortTermOperation()
        middle_term_operation = MiddleTermOperation()
        long_term_operation = LongTermOperation()

        # S4: Functions scheduling
        sched = BlockingScheduler()
        # 1) real-time simulation
        sched.add_job(lambda: real_time_simulation.run(microgrid, session, session_short),'cron', minute='0-59', second='*/5')
        # 2) short-term operation
        sched.add_job(lambda: short_term_operation.run(microgrid_short, session_short),'cron', minute='*/1', second='1')
        # 3) middle-term operation
        sched.add_job(lambda: middle_term_operation.run(microgrid_middle, session_middle),'cron', minute='*/5', second='5')
        # 4) long-term operation
        sched.add_job(lambda: long_term_operation.run(microgrid_long, session_long),'cron', minute='*/30', second='30')
        # 5) start simulation
        sched.start()

        # for i in range(1):
        #     # 1) real-time simulation
        #     real_time_simulation.run(microgrid, session, session_short)# Real-time simulation has pasted test!
        #     # 2) short-term operation
        #     short_term_operation.run(microgrid_short, session_short)  # Short-term operation has pasted test!
        #     # 3) middle-term operation
        #     middle_term_operation.run(microgrid_middle, session_middle) # Middle-term operation has pasted test!
            # 4) long-term operation
            # long_term_operation.run(microgrid_long, session_long) # Long-term operation needs to be tested!


def run():
    # Define the local models
    # Start the information connection
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    socket_upload = context.socket(zmq.REQ)
    socket_upload.connect("tcp://localhost:5556")

    socket_upload_ed = context.socket(zmq.REQ)
    socket_upload_ed.connect("tcp://localhost:5557")

    socket_upload_uc = context.socket(zmq.REQ)
    socket_upload_uc.connect("tcp://localhost:5558")

    socket_download = context.socket(zmq.REP)
    socket_download.connect("tcp://localhost:5559")

    initialize = Main(socket)
    initialize.local_ems()# The local version of EMS
    # session_short = initialize.Session()
    # session_middle = initialize.Session()
    # session_long = initialize.Session()
    #
    # info_ed = dynamic_information_pb2.microgrid()  # Dynamic information for economic dispatch
    # info_uc = dynamic_information_pb2.microgrid()  # Dynamic information for unit commitment
    # info_opf = single_period_information_pb2.microgrid()  # Optimal power flow modelling
    # local_model_short = initialize.microgrid

    # # By short-term operation process
    # logger.info("The short-term process in local ems starts!")
    # sched_lems = BlockingScheduler()  # The schedulor for the optimal power flow
    # sched_lems.add_job(
    #     lambda: short_term_operation.short_term_operation_lems(local_model_short, socket_upload, socket_download,
    #                                                            info_opf,
    #                                                            session_lems_short),
    #     'cron', minute='0-59', second='1')  # The operation is triggered minutely
    #
    # logger.info("The middle-term process in local EMS starts!")
    # sched_lems.add_job(
    #     lambda: middle_term_operation.middle_term_operation_lems(local_model_middle, socket_upload_ed, socket_download,
    #                                                              info_ed,
    #                                                              session_lems_middle),
    #     'cron', minute='*/5', second='5')  # The operation is triggered every five minute
    #
    # logger.info("The long term process in local EMS starts!")
    # sched_lems.add_job(
    #     lambda: long_term_operation.long_term_operation_lems(local_model_long, socket_upload_uc, socket_download,
    #                                                          info_uc,
    #                                                          session_lems_long),
    #     'cron', minute='*/30', second='30')  # The operation is triggered every half an hour
    # sched_lems.start()
    # for i in range(10):
    # #     long_term_operation.long_term_operation_lems(local_model_long, socket_upload_uc, socket_download, info_uc,
    # #                                                               session_lems_long)
    # #     middle_term_operation.middle_term_operation_lems(local_model_middle, socket_upload_ed, socket_download, info_ed,
    # #                                                      session_lems_middle)
    #     short_term_operation_lems(local_model_short, socket_upload, socket_download, info_opf, session_short, logger)



if __name__ == "__main__":
    # Start the main process of local energy management system
    run()

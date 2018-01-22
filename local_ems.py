# The main entrance of local energy management system (UEMS)
# Date: 4/Sep/2017
# Authors: Tianyang Zhao
# Mail: zhaoty@ntu.edu.sg
from apscheduler.schedulers.blocking import BlockingScheduler  # Time scheduler
import zmq  # The package for information and communication
from start_up import start_up_lems
from modelling.information import static_information_pb2 as static_info
from modelling.information import dynamic_information_pb2,single_period_information_pb2

from short_term_operation.main import short_term_operation_lems
# from economic_dispatch.main import middle_term_operation
# from unit_commitment.main import long_term_operation

from utils import Logger
from configuration.configuration_global import default_operation_mode

logger = Logger("local_ems")

class Main():
    """
    The main class of local energy management system
    """
    def __init__(self,socket):
        """
        :param socket: The input socket of local ems
        """
        from start_up import app
        self.socket = socket
        self.logger = Logger("local ems start up")
        ems_main = app.start_up_lems(socket)
        self.Operation_mode = ems_main.run()

        self.microgrid = start_up_lems.start_up() # Generate local ems models

        if self.Operation_mode == default_operation_mode["UEMS"]:
            self.status = ems_main.information_send(self.microgrid, static_info)

        self.Session = ems_main.database_start_up()


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
    session_short = initialize.Session()
    session_middle = initialize.Session()
    session_long = initialize.Session()

    info_ed = dynamic_information_pb2.microgrid()  # Dynamic information for economic dispatch
    info_uc = dynamic_information_pb2.microgrid()  # Dynamic information for unit commitment
    info_opf = single_period_information_pb2.microgrid()  # Optimal power flow modelling
    local_model_short = initialize.microgrid

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
    for i in range(10):
    #     long_term_operation.long_term_operation_lems(local_model_long, socket_upload_uc, socket_download, info_uc,
    #                                                               session_lems_long)
    #     middle_term_operation.middle_term_operation_lems(local_model_middle, socket_upload_ed, socket_download, info_ed,
    #                                                      session_lems_middle)
        short_term_operation_lems(local_model_short, socket_upload, socket_download, info_opf, session_short, logger)






if __name__ == "__main__":
    ## Start the main process of local energy management system
    run()

"""
Main entrance for the information management
"""
from information_management.information_send_receive import information_receive, information_send
from information_management.informulation_formulation_update import static_information_formulation, static_information_update
from information_management.informulation_formulation_update import single_period_information_formulation, single_period_information_update
from information_management.informulation_formulation_update import multiple_periods_information_formulation,multiple_periods_information_update
from utils import Logger
import threading

class information_send_receive():
    def __init__(self, socket, info):
        self.logger = Logger('Information send and receive')
        if type(info) is bytes:
            self.information_type = 0 # The default type is binary
        else:
            self.information_type = 1  # The default type is

        self.socket = socket
        self.information = info

    def send(self):
        information_send(self.socket, self.information, self.information_type)
        return 0

    def receive(self):
        info = information_receive(self.socket, self.information, self.information_type)
        return info

class Static_information_formulation_thread(threading.Thread):
    # Thread operation with time control and return value
    def __init__(self, microgrid, info):
        threading.Thread.__init__(self)
        self.info = info
        self.microgrid = microgrid
    def run(self):
        self.microgrid = static_information_formulation(self.microgrid, self.info)

class Static_information_update_thread(threading.Thread):
    # Thread operation with time control and return value
    def __init__(self, microgrid, info):
        threading.Thread.__init__(self)
        self.info = info
        self.microgrid = microgrid
        self.logger = Logger('Static information')
    def run(self):
        self.microgrid = static_information_update(self.microgrid, self.info, self.logger)

class Single_period_information_formulation_thread(threading.Thread):
    # Thread operation with time control and return value
    def __init__(self, microgrid, info ,Target_time):
        threading.Thread.__init__(self)
        self.info = info
        self.microgrid = microgrid
        self.Target_time = Target_time
    def run(self):
        self.dynamic_info = single_period_information_formulation(self.microgrid,self.info,self.Target_time)

class Single_period_information_update_thread(threading.Thread):
    # Thread operation with time control and return value
    def __init__(self, microgrid, info, socket, T):
        threading.Thread.__init__(self)
        self.info = info
        self.microgrid = microgrid
        self.socket = socket
        self.T = T
    def run(self):
        info = information_receive(self.socket, self.info, 1)
        self.microgrid = single_period_information_update(self.microgrid, info)

class MultiplePeriodsInformationFormulationThread(threading.Thread):
    # Thread operation with time control and return value
    def __init__(self, microgrid, info, Target_time, T):
        threading.Thread.__init__(self)
        self.info = info
        self.microgrid = microgrid
        self.Target_time = Target_time
        self.T = T
    def run(self):
        self.microgrid = multiple_periods_information_formulation(self.microgrid,self.info,self.Target_time, self.T)

class MultiplePeriodsInformationUpdateThread(threading.Thread):
    """
    Information collection and update thread for the universal energy management system
    """
    def __init__(self, microgrid, info, socket):
        """
        Initialize the
        :param microgrid:
        :param info:
        :param socket:
        """
        threading.Thread.__init__(self)
        self.info = info
        self.microgrid = microgrid
        self.socket = socket
    def run(self):
        info = information_receive(self.socket, self.info, 1)
        self.microgrid = multiple_periods_information_update(self.microgrid, info)
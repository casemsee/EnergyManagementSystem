"""
Main entrance for start up of energy management system
"""
from information_management.app import information_send_receive
from information_management.informulation_formulation_update import static_information_formulation,static_information_update
from configuration.configuration_global import default_operation_mode
import time
from utils import Logger
from database_management.database_functions import db_session
from configuration.configuration_database import scheduling_plan,scheduling_plan_local
import threading
class StartUpUEms():
    """
    Start up class of universal energy management system
    """
    def __init__(self,socket):
        self.t0 = time.time()
        self.Conenction_time_max = 100
        self.logger = Logger("Universal_ems_start_up")
        self.Operation_mode = default_operation_mode["UEMS"]  # 1=Work as a universal EMS; 2=Work as a local EMS.
        self.socket = socket

    def run(self):
        """
        Communication check of the neighboring MGs
        :return: Operation mode
        """
        while True:
            message = self.socket.recv()
            if message == b"ConnectionRequest":
                self.logger.info("The connection between the local EMS and universal EMS establishes!")
                self.socket.send(b"Start!")
                break
            else:
                self.logger.error("Waiting for the connection between the local EMS and universal EMS!")
                time.sleep(1)  # Waiting for next time connection

            if time.time() > self.t0 + self.Conenction_time_max:  # Timeout error detection
                self.logger.error("Connection is timeout!")
                self.logger.warning("EMS works as a local ems now!")
                self.Operation_mode = default_operation_mode["LEMS"]  # Change the working mode of universal energy management system
                break

        return self.Operation_mode

    def information_collection(self, microgrid, static_info):
        """
        Collection information from local energy management systems
        :param microgrid: static information models of energy management system
        :param static_info: information model of static information models
        :return:
        """
        info_received = information_send_receive(self.socket,static_info)

        static_info_received = info_received.receive()

        microgrid = static_information_update(microgrid, static_info_received, self.logger)

        return microgrid

    def database_start_up(self):
        """
        Create database session for the universal energy management system
        :return: Session class
        """
        Session = db_session(scheduling_plan)

        return Session


class StartUpLems():
    """
    Start up of local energy management system
    """
    def __init__(self,socket):
        self.t0 = time.time()
        self.Conenction_time_max = 1
        self.logger = Logger("Local_ems_start_up")
        self.Operation_mode = default_operation_mode["UEMS"]  # 1=Work as a universal EMS; 2=Work as a local EMS.
        self.socket = socket

    def run(self):
        """
        Communication check of the neighboring MGs
        :return: Operation mode
        """
        self.socket.send(b"ConnectionRequest")
        connection_thread = ConnectionThread(self.socket)
        connection_thread.daemon = True
        connection_thread.start()
        connection_thread.join(self.Conenction_time_max)

        try:
            if connection_thread.message == b"Start!":
                self.logger.info("The connection between the local EMS and universal EMS establishes!")
        except:
            self.logger.error("Connection is timeout!")
            self.logger.warning("EMS works as a local ems now!")
            self.Operation_mode = default_operation_mode["LEMS"]  # Change the working mode of universal energy management system

        return self.Operation_mode

    def information_send(self, microgrid, static_info):
        """
        Collection information from local energy management systems
        :param microgrid: static information models of energy management system
        :param static_info: information model of static information models
        :return: the status of information sent
        """
        static_info_formulated = static_information_formulation(microgrid, static_info)

        info_send = information_send_receive(self.socket, static_info_formulated)

        static_info_status = info_send.send()

        return static_info_status

    def database_start_up(self):
        """
        Create database session for the local energy management system
        :return: Session class
        """
        Session = db_session(scheduling_plan_local)
        return Session

class ConnectionThread(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        self.message = self.socket.recv()
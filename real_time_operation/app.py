from utils import Logger
from real_time_operation.main import measurement_data,scheduling_data,real_time_simulation,database_management
import time

class RealTimeSimulation():
    """
    Real time simulation class for one microgrid
    The calculation method is the same within the function of real time balancing(RTB/AGC)
    It should be noted that, other calculation method can be applied as well.
    1) Measurement information update
    2) Scheduling information update
    3) Real-time simulation (database management)
    """
    def __init__(self):
        self.name = "Real_time_simulation"
        self.logger = Logger("Real_time_simulation")

    def run(self, microgrid, session_scheduling, session_rtc):
        # Simulation time of real-time-simulations
        t0 = int(time.time())

        # obtain information from the measurement database (resources manager)
        microgrid = measurement_data(microgrid, session_rtc , t0)

        # obtain scheduling information from the short-term operation process (short-term-operation)
        microgrid = scheduling_data(microgrid, session_scheduling, t0)

        # run the real-time simulation (real-time-operation)
        real_time_simulation(microgrid, session_rtc, t0, self.logger)

        # maintance the database, only keep record the most recent one hour data
        database_management(session_rtc,t0)
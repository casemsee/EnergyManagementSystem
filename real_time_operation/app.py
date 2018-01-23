from utils import Logger
from real_time_operation.main import measurement_data,scheduling_data,real_time_simulation
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
        self.name = "Real time operation"
        self.logger = Logger("Real time simulation")

    def run(self, microgrid, session_scheduling, session_rtc):
        t0 = int(time.time()) # Simulation time of real-time-simulations
        microgrid = measurement_data(microgrid, session_rtc , t0)
        microgrid = scheduling_data(microgrid, session_scheduling, t0)
        real_time_simulation(microgrid, session_rtc, t0, self.logger)
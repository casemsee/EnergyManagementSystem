from copy import deepcopy
from modelling.devices import transmission_lines

def start_up(microgrid):
    """
    Start up of universal energy management system, which is depended on the start up of local energy management system.
    :param local ems model :  (short)
    :return: universal ems model (short)
    """
    microgrid = deepcopy(microgrid)

    microgrid["LINE"] = deepcopy(transmission_lines.Line)

    return microgrid
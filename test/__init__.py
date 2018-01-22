"""
Test functions for the energy management system
"""
from modelling.devices import generators, loads, energy_storage_systems, convertors  # Import modellings
from modelling.database.database_format import db_short_term, db_middle_term, db_long_term

microgrid = {"DG": generators.Generator_AC.copy(),
             "UG": generators.Generator_AC.copy(),
             "Load_ac": loads.Load_AC.copy(),
             "Load_nac": loads.Load_AC.copy(),
             "BIC": convertors.BIC.copy(),
             "ESS": energy_storage_systems.BESS.copy(),
             "PV": generators.Generator_RES.copy(),
             "WP": generators.Generator_RES.copy(),
             "Load_dc": loads.Load_DC.copy(),
             "Load_ndc": loads.Load_DC.copy(),
             "PMG": 0,
             "V_DC": 0}

class MG():
    def __init__(self):
        self.name = "Microgrid"

import inspect
variables = [i for i in dir(db_short_term) if not callable(i) ]

print(db_short_term.__dict__.keys())
print(dir(db_short_term))
print(variables)

for i in microgrid.keys():
    setattr(MG,i,microgrid[i])
    print(getattr(MG,i))
x = MG.__dict__

# print(MG.__dict__)

from CIM14.IEC61970.LoadModel import \
    ConformLoad, ConformLoadGroup, LoadArea, ConformLoadSchedule

# AC_load = ConformLoad.
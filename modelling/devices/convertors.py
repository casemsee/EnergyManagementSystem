"""
Convertor models for universal energy management system
The models include the following types of convertors.
1) AC 2 DC convertors
2) DC 2 DC convertors
"""

import configuration.configuration_convertors as default_parameters
BIC = \
    {
        "ID": default_parameters.BIC["AREA"], # Static information
        "SMAX": default_parameters.BIC["SMAX"], # Static information
        "EFF_AC2DC": default_parameters.BIC["EFF_AC2DC"], # Static information
        "EFF_DC2AC": default_parameters.BIC["EFF_DC2AC"], # Static information
        "STATUS": default_parameters.BIC["STATUS"], # Measurement information
        "P_AC2DC":default_parameters.BIC["P_AC2DC"], # Measurement information
        "P_DC2AC":default_parameters.BIC["P_DC2AC"],# Measurement information
        "Q_AC":default_parameters.BIC["COMMAND_DC2AC"],# Measurement information
        "TIME_GENERATED": default_parameters.BIC["TIME_GENERATED"], # Dynamic information
        "TIME_APPLIED": default_parameters.BIC["TIME_APPLIED"], # Dynamic information
        "TIME_COMMANDED": default_parameters.BIC["TIME_COMMANDED"], # Dynamic information
        "COMMAND_AC2DC":default_parameters.BIC["COMMAND_AC2DC"], # Dynamic information
        "COMMAND_DC2AC":default_parameters.BIC["COMMAND_DC2AC"], # Dynamic information
        "COMMAND_Q":default_parameters.BIC["COMMAND_DC2AC"],# Dynamic information
    }

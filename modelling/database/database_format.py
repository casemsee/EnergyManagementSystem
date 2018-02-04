## The database format for universal energy management system.
## As there are three processes in the the operation, there are three tablets for all processes.
## For each equipment, the operation status in specific operation process is recorded as well.
## The following parameters are required to be recorded in the database.
## The naming of the database follow the following rules.
## 1)G represents the injection.
## 2)D represents the absorption.
## 3)AC represents for the alternative current.
## 4)DC represents for the direct current.
## 5)U represents for the uncritical.
## 6)P represents for the active power.
## 7)Q represents for the reactive power.

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, FLOAT, INTEGER, String
from sqlalchemy.dialects.mysql import DATETIME

Base = declarative_base()


class db_long_term_forecasting(Base):
    # Long-term forecasting results.(For unit commitment.)
    __tablename__ = 'long_term_forecasting'

    # The unique and primary key in long term forecasting.
    TIME_STAMP = Column(INTEGER, primary_key=True)

    # Load group.
    AC_PD = Column(FLOAT)
    NAC_PD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    NDC_PD = Column(FLOAT)

    # Renewable energy group.
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)

    # Price information.
    PRICE = Column(FLOAT)


class db_mid_term_forecasting(Base):
    # Mid-term forecasting results.(For economic dispatch.)
    __tablename__ = 'mid_term_forecasting'

    # The unique and primary key in long term forecasting.
    TIME_STAMP = Column(INTEGER, primary_key=True)

    # Load group.
    AC_PD = Column(FLOAT)
    NAC_PD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    NDC_PD = Column(FLOAT)

    # Renewable energy group.
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)

    # Price information.
    PRICE = Column(FLOAT)


class db_short_term_forecasting(Base):
    # Short-term forecasting results.(For optimal power flow.)
    __tablename__ = 'short_term_forecasting'

    # The unique and primary key in long term forecasting.
    TIME_STAMP = Column(INTEGER, primary_key=True)

    # Load group.
    AC_PD = Column(FLOAT)
    NAC_PD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    NDC_PD = Column(FLOAT)

    # Renewable energy group.
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)

    # Price information.
    PRICE = Column(FLOAT)


class db_long_term(Base):
    # Long_term operation database format.
    __tablename__ = 'long_term_operation'
    TIME_STAMP = Column(INTEGER, primary_key=True)  # The primary and unique key in the database.
    # Forecasting results group.
    # Load group.
    AC_PD = Column(INTEGER)
    NAC_PD = Column(INTEGER)
    DC_PD = Column(INTEGER)
    NDC_PD = Column(INTEGER)
    # Renewable energy group.
    PV_PG = Column(INTEGER)
    WP_PG = Column(INTEGER)
    PRICE = Column(FLOAT)
    # Schedulable sources group.
    # AC side
    # Generations
    DG_STATUS = Column(INTEGER)
    DG_PG = Column(INTEGER)
    # Utility grid.
    UG_STATUS = Column(INTEGER)
    UG_PG = Column(INTEGER)
    # BIC
    BIC_PG = Column(INTEGER)
    # DC side
    # Battery.
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    # The universal energy management settings. If it is a local version, these parameters will not be generated.
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)
    # Emergency operation
    # Renewable energy curtailment.
    PV_CURT = Column(INTEGER)
    WP_CURT = Column(INTEGER)
    # Load shedding.
    AC_SHED = Column(INTEGER)
    NAC_SHED = Column(INTEGER)
    DC_SHED = Column(INTEGER)
    NDC_SHED = Column(INTEGER)
    # Cost
    COST = Column(FLOAT)


class db_middle_term(Base):
    # Mid_term operation database format.
    __tablename__ = 'mid_term_operation'
    TIME_STAMP = Column(INTEGER, primary_key=True)  # The primary and unique key in the database.
    # Forecasting results group.
    # Load group.
    AC_PD = Column(INTEGER)
    NAC_PD = Column(INTEGER)
    DC_PD = Column(INTEGER)
    NDC_PD = Column(INTEGER)
    # Renewable energy group.
    PV_PG = Column(INTEGER)
    WP_PG = Column(INTEGER)
    PRICE = Column(FLOAT)
    # Schedulable sources group.
    # AC side
    # Generations
    DG_STATUS = Column(INTEGER)
    DG_PG = Column(INTEGER)
    # Utility grid.
    UG_STATUS = Column(INTEGER)
    UG_PG = Column(INTEGER)
    # BIC
    BIC_PG = Column(INTEGER)
    # DC side
    # Battery.
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    # The universal energy management settings. If it is a local version, these parameters will not be generated.
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)
    # Emergency operation
    # Renewable energy curtailment.
    PV_CURT = Column(INTEGER)
    WP_CURT = Column(INTEGER)
    # Load shedding.
    AC_SHED = Column(INTEGER)
    NAC_SHED = Column(INTEGER)
    DC_SHED = Column(INTEGER)
    NDC_SHED = Column(INTEGER)
    # Cost
    COST = Column(FLOAT)


class db_short_term(Base):
    # The database format of optimal power flow.
    __tablename__ = 'short_term_operation'

    TIME_STAMP = Column(INTEGER, primary_key=True)  # The primary and unique key in the database.
    # Forecasting results group.
    # Load group.
    AC_PD = Column(INTEGER)
    AC_QD = Column(INTEGER)
    NAC_PD = Column(INTEGER)
    NAC_QD = Column(INTEGER)
    DC_PD = Column(INTEGER)
    NDC_PD = Column(INTEGER)
    # Renewable energy group.
    PV_PG = Column(INTEGER)
    WP_PG = Column(INTEGER)
    # Schedulable sources group.
    # AC side
    # Generations
    DG_STATUS = Column(INTEGER)
    DG_PG = Column(INTEGER)
    DG_QG = Column(INTEGER)
    # Utility grid.
    UG_STATUS = Column(INTEGER)
    UG_PG = Column(INTEGER)
    UG_QG = Column(INTEGER)
    # BIC
    BIC_PG = Column(INTEGER)
    BIC_QG = Column(INTEGER)
    # DC side
    # Battery.
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    # The universal energy management settings. If it is a local version, these parameters will not be generated.
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)
    # Emergency operation
    # Renewable energy curtailment.
    PV_CURT = Column(INTEGER)
    WP_CURT = Column(INTEGER)
    # Load shedding.
    AC_SHED = Column(INTEGER)
    NAC_SHED = Column(INTEGER)
    DC_SHED = Column(INTEGER)
    NDC_SHED = Column(INTEGER)
    # Cost
    COST = Column(FLOAT)


class db_real_time(Base):
    # The database format of optimal power flow.
    __tablename__ = 'real_time_operation'

    TIME_STAMP = Column(INTEGER, primary_key=True)  # The primary and unique key in the database.
    # Forecasting results group.
    # Load group.
    AC_PD = Column(INTEGER)
    AC_QD = Column(INTEGER)
    NAC_PD = Column(INTEGER)
    NAC_QD = Column(INTEGER)
    DC_PD = Column(INTEGER)
    NDC_PD = Column(INTEGER)
    # Renewable energy group.
    PV_PG = Column(INTEGER)
    WP_PG = Column(INTEGER)
    # Schedulable sources group.
    # AC side
    # Generations
    DG_STATUS = Column(INTEGER)
    DG_PG = Column(INTEGER)
    DG_QG = Column(INTEGER)
    # Utility grid.
    UG_STATUS = Column(INTEGER)
    UG_PG = Column(INTEGER)
    UG_QG = Column(INTEGER)
    # BIC
    BIC_PG = Column(INTEGER)
    BIC_QG = Column(INTEGER)
    # DC side
    # Battery.
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    # The universal energy management settings. If it is a local version, these parameters will not be generated.
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)
    # Emergency operation
    # Renewable energy curtailment.
    PV_CURT = Column(INTEGER)
    WP_CURT = Column(INTEGER)
    # Load shedding.
    AC_SHED = Column(INTEGER)
    NAC_SHED = Column(INTEGER)
    DC_SHED = Column(INTEGER)
    NDC_SHED = Column(INTEGER)
    # Cost
    COST = Column(FLOAT)


class db_load_profile(Base):
    # Load profile format
    __tablename__ = 'USA_FL_NASA'

    # The data is obtained from NASA.
    TIME_STAMP = Column(INTEGER, primary_key=True)

    Electricity = Column(FLOAT)
    Gas = Column(FLOAT)

    Heating_electricity = Column(FLOAT)
    Heating_gas = Column(FLOAT)
    Cooling = Column(FLOAT)

    HVACFan = Column(FLOAT)
    HVAC_electricity = Column(FLOAT)
    Fans = Column(FLOAT)

    InteriorLights = Column(FLOAT)
    ExteriorLights = Column(FLOAT)
    InteriorEquipment = Column(FLOAT)

    Misc = Column(FLOAT)
    WaterSystems = Column(FLOAT)


class weather_station(Base):
    # Weather station data format
    __tablename__ = 'ISSData'

    # The data is obtained from NASA.
    ReceiverRecID = Column(INTEGER, primary_key=True)

    ChannelIndex = Column(FLOAT)
    RecDateTime = Column(DATETIME)

    TempOut = Column(INTEGER)
    HiTempOut = Column(INTEGER)
    LowTempOut = Column(INTEGER)

    HumOut = Column(INTEGER)
    WindSpeed = Column(INTEGER)
    ScalerAvgWindDir = Column(INTEGER)

    HiWindSpeed = Column(INTEGER)
    HiWindDir = Column(INTEGER)
    DominantDir = Column(INTEGER)
    DewPoint = Column(INTEGER)

    LowWindChill = Column(INTEGER)
    HeatIndex = Column(INTEGER)

    THSWIndex = Column(INTEGER)
    RainCollectorType = Column(INTEGER)
    RainCollectorInc = Column(INTEGER)
    TotalRainClicks = Column(INTEGER)
    HiRainRate = Column(INTEGER)
    ET = Column(INTEGER)
    UV = Column(INTEGER)
    HiUV = Column(INTEGER)
    SolarRad = Column(INTEGER)
    HiSolarRad = Column(INTEGER)
    IntervalIndex = Column(INTEGER)


class hourly_history_data(Base):
    # hourly data
    __tablename__ = 'hourly_data'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    AC_PD = Column(FLOAT)
    AC_QD = Column(FLOAT)
    NAC_PD = Column(FLOAT)
    NAC_QD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    NDC_PD = Column(FLOAT)
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)


class half_hourly_history_data(Base):
    # half hourly data
    __tablename__ = 'half_hour_data'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    AC_PD = Column(FLOAT)
    AC_QD = Column(FLOAT)
    NAC_PD = Column(FLOAT)
    NAC_QD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    NDC_PD = Column(FLOAT)
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)


class five_minutes_history_data(Base):
    # five minutes data
    __tablename__ = 'five_minutes_data'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    AC_PD = Column(FLOAT)
    AC_QD = Column(FLOAT)
    NAC_PD = Column(FLOAT)
    NAC_QD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    NDC_PD = Column(FLOAT)
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)


class one_minute_history_data(Base):
    # one minute data
    __tablename__ = 'one_minute_data'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    AC_PD = Column(FLOAT)
    AC_QD = Column(FLOAT)
    NAC_PD = Column(FLOAT)
    NAC_QD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    NDC_PD = Column(FLOAT)
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)


class long2middle(Base):
    # convert long-term operation schedule to middle-term schedule
    __tablename__ = 'long2middle'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    DG_STATUS = Column(INTEGER)
    DG_PG = Column(INTEGER)
    UG_STATUS = Column(INTEGER)
    UG_PG = Column(INTEGER)
    BIC_PG = Column(INTEGER)
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)
    PV_CURT = Column(INTEGER)
    WP_CURT = Column(INTEGER)
    AC_SHED = Column(INTEGER)
    NAC_SHED = Column(INTEGER)
    DC_SHED = Column(INTEGER)
    NDC_SHED = Column(INTEGER)


class middle2short(Base):
    # convert middle-term operation schedule to short-term operation schedule
    __tablename__ = 'middle2short'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    DG_STATUS = Column(INTEGER)
    DG_PG = Column(INTEGER)
    UG_STATUS = Column(INTEGER)
    UG_PG = Column(INTEGER)
    BIC_PG = Column(INTEGER)
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)
    PV_CURT = Column(INTEGER)
    WP_CURT = Column(INTEGER)
    AC_SHED = Column(INTEGER)
    NAC_SHED = Column(INTEGER)
    DC_SHED = Column(INTEGER)
    NDC_SHED = Column(INTEGER)


class resource_management(Base):
    # convert middle-term operation schedule to short-term operation schedule
    __tablename__ = 'resource_manager'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    AC_PD = Column(INTEGER)
    AC_QD = Column(INTEGER)
    NAC_PD = Column(INTEGER)
    NAC_QD = Column(INTEGER)
    DC_PD = Column(INTEGER)
    NDC_PD = Column(INTEGER)
    # Renewable energy group.
    PV_PG = Column(INTEGER)
    WP_PG = Column(INTEGER)
    # DG group
    DG_STATUS = Column(INTEGER)
    DG_PG = Column(INTEGER)
    DG_QG = Column(INTEGER)
    # UG group
    UG_STATUS = Column(INTEGER)
    UG_PG = Column(INTEGER)
    UG_QG = Column(INTEGER)
    # BIC group
    BIC_PG = Column(INTEGER)
    BIC_QG = Column(INTEGER)
    # Battery group
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    # Coordination group
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)


class BicDBData(Base):
    __tablename__ = 'bic_status'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(20), default='bic0')
    datetime1 = Column(DATETIME(fsp=6))
    # group 1
    AC_bus_voltage_phase_A = Column(FLOAT)
    AC_bus_voltage_phase_B = Column(FLOAT)
    AC_bus_voltage_phase_C = Column(FLOAT)

    # group 2
    AC_bus_current_A = Column(FLOAT)
    AC_bus_current_B = Column(FLOAT)
    AC_bus_current_C = Column(FLOAT)
    # group 3
    AC_bus_frequency = Column(FLOAT)
    DC_bus_voltage = Column(FLOAT)
    DC_bus_current = Column(FLOAT)

    # group 4
    DC_reference_voltage = Column(FLOAT)
    AC_reference_voltage = Column(FLOAT)
    AC_reference_frequency = Column(FLOAT)

    # group 5
    DC_VP_droop_coefficient = Column(FLOAT)
    AC_fP_droop_coefficient = Column(FLOAT)
    AC_VQ_droop_coefficient = Column(FLOAT)

    # group 6
    DC_output_power = Column(FLOAT)
    AC_output_active_power = Column(FLOAT)
    AC_output_reactive_power = Column(FLOAT)

    # group 7
    environment_temperature = Column(FLOAT)
    heat_sink_temperature = Column(FLOAT)
    device_temperature = Column(FLOAT)

    # group 8
    AC_relay_ON_OFF_status = Column(INTEGER)
    DC_relay_ON_OFF_status = Column(INTEGER)
    fault_message = Column(INTEGER)

    # group 9
    isolate_status = Column(INTEGER)
    operating_mode = Column(INTEGER)
    operation_status = Column(INTEGER)

    # group 10
    active_power_reference = Column(INTEGER)
    reactive_power_reference = Column(INTEGER)
    reactive_power_reference_rec = Column(INTEGER)


class BatteryDBData(Base):
    __tablename__ = 'battery_status'
    id = Column(INTEGER, primary_key=True, autoincrement=True)

    name = Column(String(20), default='battery')

    datetime1 = Column(DATETIME(fsp=6))

    # group 1
    INDUCTOR_CUR_CH1 = Column(FLOAT)
    INDUCTOR_CUR_CH2 = Column(FLOAT)
    INDUCTOR_CUR_CH3 = Column(FLOAT)

    # group 2
    OUTPUT_CUR = Column(FLOAT)
    REF_VOL = Column(FLOAT)
    DROOP_COEF = Column(FLOAT)

    # group 3
    CH1_ONOFF_STATUS = Column(INTEGER)
    CH2_ONOFF_STATUS = Column(INTEGER)
    CH3_ONOFF_STATUS = Column(INTEGER)

    INPUT_RELAY_STATUS = Column(INTEGER)
    OUTPUT_RELAY_STATUS = Column(INTEGER)

    BAT_MODE = Column(INTEGER)

    BAT_SOC = Column(INTEGER)
    HEATSINK_TEMP = Column(FLOAT)

    # group 4
    REF_POW = Column(FLOAT)
    BAT_VOL = Column(FLOAT)
    DC_BUS_VOL = Column(FLOAT)

    OPERATING_POW = Column(FLOAT)


class PVDBData(Base):
    __tablename__ = 'pv_status'

    id = Column(INTEGER, primary_key=True, autoincrement=True)

    name = Column(String(20), default='pv')

    datetime1 = Column(DATETIME(fsp=6), )

    # group 1
    INDUCTOR_CUR_CH1 = Column(FLOAT)
    INDUCTOR_CUR_CH2 = Column(FLOAT)
    INDUCTOR_CUR_CH3 = Column(FLOAT)

    # group 2
    CH1_VOL = Column(FLOAT)
    CH2_VOL = Column(FLOAT)
    CH3_VOL = Column(FLOAT)

    # group 3
    CH1_MODE = Column(INTEGER)
    CH1_REF_POW = Column(FLOAT)

    # group 4
    CH2_MODE = Column(INTEGER)
    CH2_REF_POW = Column(FLOAT)

    # group 5
    CH3_MODE = Column(INTEGER)
    CH3_REF_POW = Column(FLOAT)

    # group 6
    INPUT_RELAY_STATUS = Column(INTEGER)
    OUTPUT_RELAY_STATUS = Column(INTEGER)
    CH1_PRIOR = Column(INTEGER)
    CH2_PRIOR = Column(INTEGER)
    CH3_PRIOR = Column(INTEGER)

    OUTPUT_CUR = Column(FLOAT)
    DC_BUS_VOL = Column(FLOAT)

    CH1_POWER = Column(FLOAT)
    CH2_POWER = Column(FLOAT)
    CH3_POWER = Column(FLOAT)


class RMDBData(Base):
    __tablename__ = 'rm_status'
    id = Column(INTEGER, primary_key=True, autoincrement=True)

    name = Column(String(20), default='pv')

    datetime1 = Column(DATETIME(fsp=6), )
    PV0_1_VOL = Column(FLOAT)
    PV0_2_VOL = Column(FLOAT)
    PV0_3_VOL = Column(FLOAT)
    PV1_1_VOL = Column(FLOAT)
    PV1_2_VOL = Column(FLOAT)
    PV1_3_VOL = Column(FLOAT)

    BAT_VOL = Column(FLOAT)
    BAT_CURR = Column(FLOAT)
    BAT_POW = Column(FLOAT)

    LOAD_DC_CT_VOL = Column(FLOAT)
    LOAD_DC_CT_CURR = Column(FLOAT)
    LOAD_DC_CT_POW = Column(FLOAT)
    LOAD_DC_NCT_VOL = Column(FLOAT)
    LOAD_DC_NCT_CURR = Column(FLOAT)
    LOAD_DC_NCT_POW = Column(FLOAT)
    LOAD_AC3P_CT_VOL = Column(FLOAT)
    LOAD_AC3P_CT_ACTPOW = Column(FLOAT)
    LOAD_AC3P_CT_REACTPOW = Column(FLOAT)
    LOAD_AC3P_NCT_VOL = Column(FLOAT)
    LOAD_AC3P_NCT_ACTPOW = Column(FLOAT)
    LOAD_AC3P_NCT_REACTPOW = Column(FLOAT)

    DC_OUTLET_VOL = Column(FLOAT)
    DC_OUTLET_CURR = Column(FLOAT)
    DC_OUTLET_POW = Column(FLOAT)
    AC_OUTLET_VOL_U = Column(FLOAT)
    AC_OUTLET_VOL_V = Column(FLOAT)
    AC_OUTLET_VOL_W = Column(FLOAT)
    AC_OUTLET_CURR_U = Column(FLOAT)
    AC_OUTLET_CURR_V = Column(FLOAT)
    AC_OUTLET_FREQ = Column(FLOAT)
    AC_OUTLET_ACTPOW = Column(FLOAT)
    AC_OUTLET_REACTPOW = Column(FLOAT)

    GRID_VOL_U = Column(FLOAT)
    GRID_VOL_V = Column(FLOAT)
    GRID_VOL_W = Column(FLOAT)
    GRID_CURR_U = Column(FLOAT)
    GRID_CURR_V = Column(FLOAT)
    GRID_CURR_W = Column(FLOAT)
    GRID_FREQ = Column(FLOAT)
    GRID_ACTPOW = Column(FLOAT)
    GRID_REACTPOW = Column(FLOAT)

    DG_VOL_U = Column(FLOAT)
    DG_VOL_V = Column(FLOAT)
    DG_VOL_W = Column(FLOAT)
    DG_CURR_U = Column(FLOAT)
    DG_CURR_V = Column(FLOAT)
    DG_CURR_W = Column(FLOAT)
    DG_FREQ = Column(FLOAT)
    DG_ACTPOW = Column(FLOAT)
    DG_REACTPOW = Column(FLOAT)

    DC_VOL = Column(FLOAT)
    AC_VOL = Column(FLOAT)
    AC_FREQ = Column(FLOAT)
    TEMP_A = Column(FLOAT)
    TEMP_B = Column(FLOAT)
    TEMP_C = Column(FLOAT)
    RM_REALY_STATUS_0 = Column(INTEGER)
    RM_REALY_STATUS_1 = Column(INTEGER)
    DC_IS_STABLE = Column(INTEGER)
    AC_IS_STABLE = Column(INTEGER)
    AC_FREQ_STABLE = Column(INTEGER)
    AC_OUTLET_DIR = Column(INTEGER)
    GRID_DIR = Column(FLOAT)
    DG_DIR = Column(FLOAT)
    PV0_CH1_MODE = Column(INTEGER)
    PV0_CH2_MODE = Column(INTEGER)
    PV0_CH3_MODE = Column(INTEGER)
    PV1_CH1_MODE = Column(INTEGER)
    PV1_CH2_MODE = Column(INTEGER)
    PV1_CH3_MODE = Column(INTEGER)
    PV0_1_POW = Column(FLOAT)
    PV0_2_POW = Column(FLOAT)
    PV0_3_POW = Column(FLOAT)
    PV1_1_POW = Column(FLOAT)
    PV1_2_POW = Column(FLOAT)
    PV1_3_POW = Column(FLOAT)
    BIC_isolate_status = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    WT_MODE = Column(INTEGER)
    BAT_MODE = Column(INTEGER)
    AC_OUTLET_CURR_W = Column(FLOAT)
    BIC_AC_output_active_power = Column(FLOAT)
    BIC_AC_output_reactive_power = Column(FLOAT)

    WT_POW = Column(FLOAT)
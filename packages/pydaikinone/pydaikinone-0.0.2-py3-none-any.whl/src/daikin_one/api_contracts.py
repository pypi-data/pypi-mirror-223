from dataclasses import dataclass, field
from typing import List
import datetime
from enum import Enum

from dataclass_wizard import JSONListWizard, JSONSerializable, json_field

@dataclass
class DaikinOneAccessToken(JSONSerializable):
    access_token: str = json_field("accessToken", all=True)
    expires_in: int = json_field("accessTokenExpiresIn", all=True)
    token_type: str = json_field("tokenType", all=True)

    def is_expired(self):
        expires_at = datetime.datetime.now() + datetime.timedelta(seconds=self.expires_in - 5)
        if datetime.datetime.now() >= expires_at:
            return True
        else:
            return False

@dataclass
class DaikinOneDevice:
    id: str
    name: str
    model: str
    firmware_version: str

@dataclass
class DaikinOneLocation(JSONListWizard):
    location_name: str = json_field("locationName", all=True)
    devices: List[DaikinOneDevice]

class EquipmentStatus(Enum):
    COOL = 1
    OVERCOOL_FOR_DEHUMIDIFIER = 2
    HEAT = 3
    FAN = 4
    IDLE = 5

class ThermostatMode(Enum):
    OFF = 0
    HEAT = 1
    COOL = 2
    AUTO = 3
    EMERGENCY_HEAT = 4

class ThermostatModeLimit(Enum):
    NONE = 0
    ALL = 1
    HEAT_ONLY = 2
    COOL_ONLY = 3

class FanMode(Enum):
    AUTO = 0
    ON = 1

class FanCirculateMode(Enum):
    OFF = 0
    ALWAYS_ON = 1
    ON_A_SCHEDULE = 2

class FanCirculateSpeed(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

@dataclass
class DaikinOneThermostat(JSONSerializable):
    humidity_indoor: float = json_field("humIndoor")
    humidity_outdoor: float = json_field("humOutdoor")
    temperature_indoor: float = json_field("tempIndoor")
    temperature_outdoor: float = json_field("tempOutdoor")
    mode: ThermostatMode
    mode_limit: ThermostatModeLimit = json_field("modeLimit")
    setpoint_delta: float = json_field("setpointDelta")
    setpoint_minimum: float = json_field("setpointMinimum")
    setpoint_maximum: float = json_field("setpointMaximum")
    heat_setpoint: float = json_field("heat_setpoint")
    cool_setpoint: float = json_field("cool_setpoint")
    fan: FanMode
    fan_circulate_speed: FanCirculateSpeed = json_field("fanCirculateSpeed")
    fan_circulate: FanCirculateMode = json_field("fanCirculate")
    equipment_status: EquipmentStatus = json_field("equipmentStatus")
    equipment_communication: int = json_field("equipmentCommunication")
    emergency_heat_mode_available: bool = json_field("modeEmHeatAvailable")
    geofencing_enabled: bool = json_field("geofencingEnabled")
    schedule_enabled: bool = json_field("scheduleEnabled")
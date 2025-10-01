"""
Pydantic models for data validation and API schemas.
"""

from typing import Any
from pydantic import BaseModel, Field, ConfigDict


class AntennaColor(BaseModel):
    """RGB color for antenna LED"""

    red: int = Field(ge=0, le=255, description="Red channel (0-255)")
    green: int = Field(ge=0, le=255, description="Green channel (0-255)")
    blue: int = Field(ge=0, le=255, description="Blue channel (0-255)")


class ActionSequence(BaseModel):
    """Furby action sequence parameters"""

    input: int = Field(ge=0, le=255, description="Action input value")
    index: int = Field(ge=0, le=255, description="Action index")
    subindex: int = Field(ge=0, le=255, description="Action subindex")
    specific: int = Field(ge=0, le=255, description="Specific action ID")


class MoodUpdate(BaseModel):
    """Mood meter update parameters"""

    type: str = Field(
        description="Mood type: excitedness, displeasedness, tiredness, fullness, wellness"
    )
    action: str = Field(description="Action: set or increase")
    value: int = Field(ge=0, le=255, description="Value to set or increase by")


class DLCUpload(BaseModel):
    """DLC file upload parameters"""

    slot: int = Field(ge=0, le=255, description="DLC slot number")
    filename: str = Field(max_length=12, description="DLC filename (max 12 chars)")


class SensorData(BaseModel):
    """Sensor data from Furby"""

    model_config = ConfigDict(extra="allow")

    timestamp: float = Field(description="Unix timestamp")
    raw_data: str = Field(description="Hex-encoded raw sensor data")
    # Additional fields can be added as protocol is better understood


class FurbyStatus(BaseModel):
    """Current Furby connection status"""

    connected: bool
    device_name: str | None = None
    device_address: str | None = None
    firmware_version: str | None = None


class CommandResponse(BaseModel):
    """Generic command response"""

    success: bool
    message: str
    data: dict[str, Any] | None = None


class FurbyInfo(BaseModel):
    """Furby device information"""

    manufacturer: str | None = None
    model_number: str | None = None
    serial_number: str | None = None
    hardware_revision: str | None = None
    firmware_revision: str | None = None
    software_revision: str | None = None

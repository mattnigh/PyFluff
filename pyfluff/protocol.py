"""
Furby Connect BLE Protocol Definitions

This module contains all the BLE service and characteristic UUIDs,
as well as protocol constants for communicating with Furby Connect.

Based on reverse engineering by Jeija (bluefluff project).
"""

from enum import Enum
from typing import Final


class FurbyService:
    """Furby Connect BLE GATT Service UUIDs"""

    GENERIC_ACCESS: Final[str] = "00001800-0000-1000-8000-00805f9b34fb"
    GENERIC_ATTRIBUTE: Final[str] = "00001801-0000-1000-8000-00805f9b34fb"
    DEVICE_INFORMATION: Final[str] = "0000180a-0000-1000-8000-00805f9b34fb"
    NORDIC_DFU: Final[str] = "000015301212efde1523785feabcd123"
    FLUFF: Final[str] = "dab91435b5a1e29cb041bcd562613bde"


class FurbyCharacteristic:
    """Furby Connect BLE GATT Characteristic UUIDs"""

    # Device Information
    MANUFACTURER_NAME: Final[str] = "00002a29-0000-1000-8000-00805f9b34fb"
    MODEL_NUMBER: Final[str] = "00002a24-0000-1000-8000-00805f9b34fb"
    SERIAL_NUMBER: Final[str] = "00002a25-0000-1000-8000-00805f9b34fb"
    HARDWARE_REVISION: Final[str] = "00002a27-0000-1000-8000-00805f9b34fb"
    FIRMWARE_REVISION: Final[str] = "00002a26-0000-1000-8000-00805f9b34fb"
    SOFTWARE_REVISION: Final[str] = "00002a28-0000-1000-8000-00805f9b34fb"

    # Fluff Service - Main control characteristics
    GENERALPLUS_WRITE: Final[str] = "dab91383b5a1e29cb041bcd562613bde"
    GENERALPLUS_LISTEN: Final[str] = "dab91382b5a1e29cb041bcd562613bde"
    NORDIC_WRITE: Final[str] = "dab90757b5a1e29cb041bcd562613bde"
    NORDIC_LISTEN: Final[str] = "dab90756b5a1e29cb041bcd562613bde"
    RSSI_LISTEN: Final[str] = "dab90755b5a1e29cb041bcd562613bde"
    FILE_WRITE: Final[str] = "dab90758b5a1e29cb041bcd562613bde"
    MYSTERY_1: Final[str] = "dab91440b5a1e29cb041bcd562613bde"
    MYSTERY_2: Final[str] = "dab91441b5a1e29cb041bcd562613bde"


class GeneralPlusCommand(Enum):
    """GeneralPlus microcontroller command identifiers"""

    TRIGGER_ACTION_BY_INPUT = 0x10
    TRIGGER_ACTION_BY_INDEX = 0x11
    TRIGGER_ACTION_BY_SUBINDEX = 0x12
    TRIGGER_SPECIFIC_ACTION = 0x13
    SET_ANTENNA_COLOR = 0x14
    FURBY_MESSAGE = 0x20
    SET_NAME = 0x21
    SET_MOODMETER = 0x23
    SET_NOTIFICATIONS = 0x31
    ANNOUNCE_DLC_UPLOAD = 0x50
    DELETE_FILE = 0x53
    GET_FILE_SIZE = 0x54
    GET_CHECKSUM = 0x55
    LOAD_DLC = 0x60
    ACTIVATE_DLC = 0x61
    DEACTIVATE_DLC = 0x62
    GET_SLOT_ALLOCATION = 0x72
    GET_SLOT_INFO = 0x73
    DELETE_DLC_SLOT = 0x74
    BODY_CAM = 0xBC
    LCD_DEBUG_MENU = 0xDB
    LCD_BACKLIGHT = 0xCD
    GET_GPL_FIRMWARE = 0xFE


class GeneralPlusResponse(Enum):
    """GeneralPlus microcontroller response identifiers"""

    FURBY_MESSAGE = 0x20
    SENSOR_STATUS = 0x21
    IM_HERE_SIGNAL = 0x22
    CURRENT_MODE = 0x23
    FILE_TRANSFER_MODE = 0x24
    LANGUAGE = 0x25
    FURBIES_MET = 0x26
    GOT_FILE_SIZE = 0x54
    GOT_FILE_CHECKSUM = 0x55
    SLOTS_INFO = 0x72
    GOT_SLOT_INFO_BY_INDEX = 0x73
    GOT_DELETE_SLOT_BY_INDEX = 0x74
    REPORT_DLC = 0xDC
    GPL_FIRMWARE_VERSION = 0xFE


class FurbyMessage(Enum):
    """Furby status messages (0x20 responses)"""

    ENTERED_NAMING_MODE = 0x01
    EXITED_NAMING_MODE = 0x02
    FURBY_NAMED = 0x03
    ENTERED_APP_MODE = 0x04
    EXITED_APP_MODE = 0x05
    RESPONSE_PLAYED = 0x06
    SPEECH_PLAYING = 0x07
    SLAVE_ACK = 0x08
    MASK_ADDED = 0x0A
    MASK_REMOVED = 0x0B
    SEQUENCE_PLAYING = 0x0C
    SEQUENCE_CANCELLED = 0x0D
    SEQUENCE_ENDED = 0x0E
    INPUT_OUT_OF_RANGE = 0x0F
    INDEX_OUT_OF_RANGE = 0x10
    SUBINDEX_OUT_OF_RANGE = 0x11
    SPECIFIC_OUT_OF_RANGE = 0x12
    SLEEP_MASK_ADDED = 0x13
    SLEEP_MASK_REMOVED = 0x14
    BODYCAM_ON = 0x15
    BODYCAM_OFF = 0x16
    LCD_ON = 0x17
    LCD_OFF = 0x18
    GROUP_NOT_ACTIVE = 0x19
    TIMED_GROUP_SET = 0x1A
    CUSTOM_NOTIFICATION_SET = 0x1B


class FileTransferMode(Enum):
    """DLC file transfer status messages"""

    FILE_ALREADY_EXISTS = 0x01
    READY_TO_RECEIVE = 0x02
    FILE_TRANSFER_TIMEOUT = 0x03
    READY_TO_APPEND = 0x04
    FILE_RECEIVED_OK = 0x05
    FILE_RECEIVED_ERROR = 0x06


class MoodMeterType(Enum):
    """Furby emotional state types"""

    EXCITEDNESS = 0x00
    DISPLEASEDNESS = 0x01
    TIREDNESS = 0x02
    FULLNESS = 0x03
    WELLNESS = 0x04


class NordicCommand(Enum):
    """Nordic microcontroller command identifiers"""

    PACKET_ACK = 0x09


# Protocol constants
FURBY_NAME: Final[str] = "Furby"
MAX_PACKET_SIZE: Final[int] = 20
IDLE_INTERVAL: Final[float] = 3.0  # seconds
FILE_CHUNK_SIZE: Final[int] = 20  # bytes per BLE packet


class FurbyProtocol:
    """
    Helper class for building and parsing Furby Connect protocol packets.
    """

    @staticmethod
    def build_antenna_command(red: int, green: int, blue: int) -> bytes:
        """Build command to set antenna LED color (0-255 for each channel)"""
        return bytes([GeneralPlusCommand.SET_ANTENNA_COLOR.value, red, green, blue])

    @staticmethod
    def build_action_command(
        input: int, index: int, subindex: int, specific: int
    ) -> bytes:
        """Build command to trigger specific action"""
        return bytes(
            [
                GeneralPlusCommand.TRIGGER_SPECIFIC_ACTION.value,
                0x00,
                input,
                index,
                subindex,
                specific,
            ]
        )

    @staticmethod
    def build_lcd_command(enabled: bool) -> bytes:
        """Build command to control LCD backlight"""
        return bytes([GeneralPlusCommand.LCD_BACKLIGHT.value, 0x01 if enabled else 0x00])

    @staticmethod
    def build_debug_menu_command() -> bytes:
        """Build command to cycle through debug menus"""
        return bytes([GeneralPlusCommand.LCD_DEBUG_MENU.value])

    @staticmethod
    def build_name_command(name_id: int) -> bytes:
        """Build command to set Furby name (0-128)"""
        return bytes([GeneralPlusCommand.SET_NAME.value, name_id])

    @staticmethod
    def build_moodmeter_command(
        action: int, mood_type: MoodMeterType, value: int
    ) -> bytes:
        """
        Build command to set mood meter.
        action: 1 = set value, 0 = increase value
        mood_type: MoodMeterType enum
        value: new value (action=1) or delta (action=0)
        """
        return bytes(
            [GeneralPlusCommand.SET_MOODMETER.value, action, mood_type.value, value]
        )

    @staticmethod
    def build_dlc_announce_command(
        size: int, slot: int, filename: str
    ) -> bytes:
        """Build command to announce DLC upload"""
        # Size is 3 bytes (big-endian)
        size_bytes = bytes([(size >> 16) & 0xFF, (size >> 8) & 0xFF, size & 0xFF])
        # Filename is 12 bytes, padded with nulls
        filename_bytes = filename.encode("ascii")[:12].ljust(12, b"\x00")
        return bytes(
            [GeneralPlusCommand.ANNOUNCE_DLC_UPLOAD.value]
            + list(size_bytes)
            + [0x00, slot]
            + list(filename_bytes)
            + [0x00, 0x00]
        )

    @staticmethod
    def build_load_dlc_command(slot: int) -> bytes:
        """Build command to load DLC from slot"""
        return bytes([GeneralPlusCommand.LOAD_DLC.value, slot])

    @staticmethod
    def build_activate_dlc_command() -> bytes:
        """Build command to activate loaded DLC"""
        return bytes([GeneralPlusCommand.ACTIVATE_DLC.value])

    @staticmethod
    def build_deactivate_dlc_command(slot: int) -> bytes:
        """Build command to deactivate DLC slot"""
        return bytes([GeneralPlusCommand.DEACTIVATE_DLC.value, slot])

    @staticmethod
    def build_delete_dlc_command(slot: int) -> bytes:
        """Build command to delete DLC slot"""
        return bytes([GeneralPlusCommand.DELETE_DLC_SLOT.value, slot])

    @staticmethod
    def build_nordic_packet_ack(enabled: bool) -> bytes:
        """Build Nordic command to enable/disable packet acknowledgment"""
        return bytes([NordicCommand.PACKET_ACK.value, 0x01 if enabled else 0x00, 0x00])

    @staticmethod
    def parse_response(data: bytes) -> tuple[int, bytes]:
        """Parse response packet, returning (command_id, payload)"""
        if len(data) == 0:
            raise ValueError("Empty response packet")
        return data[0], data[1:]

    @staticmethod
    def is_furby_message(data: bytes) -> bool:
        """Check if response is a FurbyMessage (0x20)"""
        return len(data) > 0 and data[0] == GeneralPlusResponse.FURBY_MESSAGE.value

    @staticmethod
    def get_furby_message_type(data: bytes) -> FurbyMessage | None:
        """Extract FurbyMessage type from response"""
        if len(data) >= 2 and FurbyProtocol.is_furby_message(data):
            try:
                return FurbyMessage(data[1])
            except ValueError:
                return None
        return None

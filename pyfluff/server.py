"""
FastAPI web server for PyFluff.

Provides HTTP API and WebSocket support for controlling Furby Connect.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from pyfluff.furby import FurbyConnect
from pyfluff.dlc import DLCManager
from pyfluff.models import (
    ActionSequence,
    AntennaColor,
    CommandResponse,
    FurbyStatus,
    MoodUpdate,
)
from pyfluff.protocol import MoodMeterType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Global Furby instance
furby: FurbyConnect | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifespan context manager for FastAPI app."""
    global furby

    # Startup: Connect to Furby
    logger.info("PyFluff server starting up...")
    furby = FurbyConnect()

    try:
        await furby.connect()
        logger.info("Connected to Furby")
    except Exception as e:
        logger.error(f"Failed to connect to Furby: {e}")
        logger.info("Server will start but Furby is not connected")

    yield

    # Shutdown: Disconnect from Furby
    logger.info("PyFluff server shutting down...")
    if furby and furby.connected:
        await furby.disconnect()


# Create FastAPI app
app = FastAPI(
    title="PyFluff API",
    description="Modern Python controller for Furby Connect via Bluetooth LE",
    version="1.0.0",
    lifespan=lifespan,
)


# Helper function to check connection
def get_furby() -> FurbyConnect:
    """Get connected Furby instance or raise error."""
    if furby is None or not furby.connected:
        raise HTTPException(status_code=503, detail="Not connected to Furby")
    return furby


# API Endpoints


@app.get("/")
async def root() -> HTMLResponse:
    """Serve web interface."""
    web_dir = Path(__file__).parent.parent / "web"
    index_file = web_dir / "index.html"

    if index_file.exists():
        return FileResponse(index_file)
    else:
        return HTMLResponse(
            """
            <html>
                <head><title>PyFluff</title></head>
                <body>
                    <h1>PyFluff API Server</h1>
                    <p>Web interface not found. API is available at <a href="/docs">/docs</a></p>
                </body>
            </html>
            """
        )


@app.get("/status", response_model=FurbyStatus)
async def get_status() -> FurbyStatus:
    """Get current Furby connection status."""
    if furby is None:
        return FurbyStatus(connected=False)

    status = FurbyStatus(
        connected=furby.connected,
        device_name=furby.device.name if furby.device else None,
        device_address=furby.device.address if furby.device else None,
    )

    if furby.connected:
        try:
            info = await furby.get_device_info()
            status.firmware_version = info.firmware_revision
        except Exception as e:
            logger.warning(f"Could not get device info: {e}")

    return status


@app.post("/connect", response_model=CommandResponse)
async def connect() -> CommandResponse:
    """Connect to a Furby device."""
    global furby

    if furby and furby.connected:
        return CommandResponse(success=True, message="Already connected")

    try:
        furby = FurbyConnect()
        await furby.connect()
        return CommandResponse(success=True, message="Connected to Furby")
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/disconnect", response_model=CommandResponse)
async def disconnect() -> CommandResponse:
    """Disconnect from Furby."""
    fb = get_furby()
    await fb.disconnect()
    return CommandResponse(success=True, message="Disconnected")


@app.post("/antenna", response_model=CommandResponse)
async def set_antenna(color: AntennaColor) -> CommandResponse:
    """Set antenna LED color."""
    fb = get_furby()
    await fb.set_antenna_color(color.red, color.green, color.blue)
    return CommandResponse(
        success=True,
        message=f"Antenna color set to RGB({color.red}, {color.green}, {color.blue})",
    )


@app.post("/action", response_model=CommandResponse)
async def trigger_action(action: ActionSequence) -> CommandResponse:
    """Trigger a Furby action sequence."""
    fb = get_furby()
    await fb.trigger_action(action.input, action.index, action.subindex, action.specific)
    return CommandResponse(success=True, message="Action triggered")


@app.post("/lcd/{state}", response_model=CommandResponse)
async def set_lcd(state: bool) -> CommandResponse:
    """Control LCD backlight."""
    fb = get_furby()
    await fb.set_lcd_backlight(state)
    return CommandResponse(
        success=True, message=f"LCD backlight {'on' if state else 'off'}"
    )


@app.post("/debug", response_model=CommandResponse)
async def cycle_debug_menu() -> CommandResponse:
    """Cycle through debug menus."""
    fb = get_furby()
    await fb.cycle_debug_menu()
    return CommandResponse(success=True, message="Debug menu cycled")


@app.post("/name/{name_id}", response_model=CommandResponse)
async def set_name(name_id: int) -> CommandResponse:
    """Set Furby name by ID (0-128)."""
    if not 0 <= name_id <= 128:
        raise HTTPException(status_code=400, detail="Name ID must be between 0 and 128")

    fb = get_furby()
    await fb.set_name(name_id)
    return CommandResponse(success=True, message=f"Name set to ID {name_id}")


@app.post("/mood", response_model=CommandResponse)
async def set_mood(mood: MoodUpdate) -> CommandResponse:
    """Update Furby mood meter."""
    fb = get_furby()

    # Map mood type string to enum
    mood_map = {
        "excitedness": MoodMeterType.EXCITEDNESS,
        "displeasedness": MoodMeterType.DISPLEASEDNESS,
        "tiredness": MoodMeterType.TIREDNESS,
        "fullness": MoodMeterType.FULLNESS,
        "wellness": MoodMeterType.WELLNESS,
    }

    mood_type = mood_map.get(mood.type.lower())
    if mood_type is None:
        raise HTTPException(status_code=400, detail=f"Invalid mood type: {mood.type}")

    set_absolute = mood.action.lower() == "set"
    await fb.set_mood(mood_type, mood.value, set_absolute)

    return CommandResponse(
        success=True,
        message=f"Mood {mood.type} {'set to' if set_absolute else 'increased by'} {mood.value}",
    )


@app.post("/dlc/upload", response_model=CommandResponse)
async def upload_dlc(file: UploadFile, slot: int = 2) -> CommandResponse:
    """Upload a DLC file to Furby."""
    fb = get_furby()

    # Save uploaded file temporarily
    import tempfile

    with tempfile.NamedTemporaryFile(delete=False, suffix=".dlc") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        dlc_manager = DLCManager(fb)
        await dlc_manager.upload_dlc(tmp_path, slot)
        return CommandResponse(
            success=True, message=f"DLC uploaded to slot {slot}"
        )
    except Exception as e:
        logger.error(f"DLC upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        tmp_path.unlink(missing_ok=True)


@app.post("/dlc/load/{slot}", response_model=CommandResponse)
async def load_dlc(slot: int) -> CommandResponse:
    """Load DLC from slot."""
    fb = get_furby()
    dlc_manager = DLCManager(fb)
    await dlc_manager.load_dlc(slot)
    return CommandResponse(success=True, message=f"DLC loaded from slot {slot}")


@app.post("/dlc/activate", response_model=CommandResponse)
async def activate_dlc() -> CommandResponse:
    """Activate loaded DLC."""
    fb = get_furby()
    dlc_manager = DLCManager(fb)
    await dlc_manager.activate_dlc()
    return CommandResponse(success=True, message="DLC activated")


@app.post("/dlc/deactivate/{slot}", response_model=CommandResponse)
async def deactivate_dlc(slot: int) -> CommandResponse:
    """Deactivate DLC slot."""
    fb = get_furby()
    dlc_manager = DLCManager(fb)
    await dlc_manager.deactivate_dlc(slot)
    return CommandResponse(success=True, message=f"DLC slot {slot} deactivated")


@app.post("/dlc/delete/{slot}", response_model=CommandResponse)
async def delete_dlc(slot: int) -> CommandResponse:
    """Delete DLC from slot."""
    fb = get_furby()
    dlc_manager = DLCManager(fb)
    await dlc_manager.delete_dlc(slot)
    return CommandResponse(success=True, message=f"DLC slot {slot} deleted")


@app.websocket("/ws/sensors")
async def websocket_sensors(websocket: WebSocket) -> None:
    """WebSocket endpoint for streaming sensor data."""
    await websocket.accept()
    logger.info("WebSocket client connected")

    try:
        fb = get_furby()

        async for sensor_data in fb.sensor_stream():
            await websocket.send_json(sensor_data.model_dump())

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "pyfluff.server:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=False,
    )

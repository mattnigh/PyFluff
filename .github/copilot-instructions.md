# GitHub Copilot Instructions for PyFluff

## Project Overview

PyFluff is a modern Python 3.11+ implementation for controlling Furby Connect toys via Bluetooth Low Energy (BLE). It's a complete rewrite of the original [bluefluff](https://github.com/Jeija/bluefluff) Node.js project, targeting Raspberry Pi OS (Bookworm) and other Linux systems.

### Core Purpose
- Control Furby Connect toys via BLE (antenna color, actions, moods, sensors)
- Upload and manage DLC (DownLoadable Content) files
- Provide REST API, WebSocket, CLI, and Python library interfaces
- Monitor real-time sensor data (accelerometer, touch sensors, joystick)

## Technology Stack

### Core Dependencies
- **Python**: 3.11+ (uses modern type hints, async/await patterns)
- **Bleak** (0.21+): Modern, cross-platform BLE library (replaces deprecated Noble)
- **FastAPI**: Async web framework with automatic OpenAPI documentation
- **Uvicorn**: ASGI server for FastAPI
- **Pydantic v2**: Data validation with type safety
- **Typer**: Modern CLI framework
- **Rich**: Terminal formatting and progress bars

### Development Tools
- **pytest**: Testing framework
- **mypy**: Static type checking
- **ruff**: Fast Python linter
- **black**: Code formatting

## Architecture

### Module Structure
```
pyfluff/
├── __init__.py          # Package exports
├── protocol.py          # BLE protocol definitions (UUIDs, enums, packet builders)
├── furby.py            # FurbyConnect class (main BLE interface)
├── models.py           # Pydantic data models for validation
├── dlc.py              # DLC file upload manager
├── server.py           # FastAPI web server with REST + WebSocket
├── cli.py              # Typer CLI commands
└── __main__.py         # Server entry point

web/
├── index.html          # Main web interface
├── style.css           # Light, colorful, modern theme with gradients
├── app.js              # Frontend logic (mood sliders, antenna controls, API calls)
├── actions.js          # Action database with 1400+ Furby actions
└── names.js            # Name database with 129 Furby names
```

### Key Classes

#### `FurbyConnect` (furby.py)
- Main async context manager for BLE connection
- Methods: `discover()`, `connect()`, `disconnect()`
- Commands: `set_antenna_color()`, `trigger_action()`, `set_mood()`, etc.
- Notification handlers for sensor data streaming

#### `FurbyProtocol` (protocol.py)
- Static methods for building BLE command packets
- Enums for commands, responses, mood types
- Service/characteristic UUID definitions

#### `DLCManager` (dlc.py)
- Handles DLC file uploads with chunking (20-byte packets)
- Methods: `upload_dlc()`, `load_dlc()`, `activate_dlc()`, `delete_dlc()`
- Progress tracking for large file transfers

#### `PyFluffServer` (server.py)
- FastAPI app with REST endpoints and WebSocket
- Connection state management
- Real-time sensor streaming via WebSocket

### Web Interface

#### Frontend Architecture (`web/`)
- **Vanilla JavaScript** - No frameworks, modern async/await patterns
- **Light Theme** - Colorful gradients with sparkle effects
- **Real-time Updates** - Mood sliders auto-send on release, status polling every 10s
- **Auto-generated Action Database** - 1400+ actions parsed from `docs/actionlist.md`

#### Key Files

**index.html**
- Mood Control: 5 sliders (Excitedness, Displeasedness, Tiredness, Fullness, Wellness)
- Antenna Color: RGB sliders with color preview, 8 presets + 5 memory slots
- Custom Action: Searchable dropdown with 1400+ actions, recent actions tracking
- Quick Actions: Giggle, Puke, LCD controls, Debug menu
- Sensor Monitor: WebSocket-based real-time streaming

**style.css**
- CSS Grid layouts with `minmax()` for perfect alignment
- Gradient backgrounds: `linear-gradient(135deg, #fef3c7, #fce7f3, #e0e7ff)`
- Glass morphism effects with `backdrop-filter: blur(10px)`
- Z-index hierarchy: cards(1-2), dropdowns(9999)
- Compact spacing (reduced 25-40% from original)

**app.js**
- Mood sliders: Auto-update on `change` event, resend on 0/100 click-release
- Antenna color: Auto-send on slider input, clickable preview to resend
- Color memory: 5 recent colors with random bright initialization
- Cookie storage for persistent preferences
- API calls: `async apiCall(endpoint, method, body)` wrapper

**actions.js (AUTO-GENERATED)**
- **DO NOT EDIT MANUALLY** - Run `scripts/generate_actions_js.py` to regenerate
- 1439 actions parsed from `docs/actionlist.md`
- Categories: Generic reactions, World App, Octave Notes, etc. (NO numeric prefixes)
- Search functionality: Filter by category, description, or coordinates
- Recent actions: Cookie-based tracking (max 10, 365-day expiry)
- Real-time description updates on input field changes

## Coding Standards

### Type Hints
- **ALWAYS** use type hints for all function parameters and return values
- Use `Optional[T]` for nullable values
- Use `Union[T1, T2]` or `T1 | T2` for multiple types
- Use generic types: `List[T]`, `Dict[K, V]`

```python
async def set_antenna_color(self, red: int, green: int, blue: int) -> None:
    """Set antenna LED color (0-255 for each channel)."""
```

### Async/Await Pattern
- **ALL** BLE operations are async
- Use `async def` for any function calling BLE methods
- Use `await` for all async calls
- Use `async with` for context managers

```python
async def connect(self, address: str, timeout: float = 10.0) -> None:
    async with asyncio.timeout(timeout):
        await self._client.connect()
```

### Pydantic Models
- Use Pydantic v2 `BaseModel` for all request/response data
- Use `Field()` for validation and descriptions
- Configure with `ConfigDict(frozen=True)` for immutable models

```python
from pydantic import BaseModel, Field

class AntennaColor(BaseModel):
    """RGB color for Furby's antenna LED."""
    red: int = Field(ge=0, le=255, description="Red channel (0-255)")
    green: int = Field(ge=0, le=255, description="Green channel (0-255)")
    blue: int = Field(ge=0, le=255, description="Blue channel (0-255)")
```

### Error Handling
- Raise descriptive exceptions with context
- Use `asyncio.TimeoutError` for timeout failures
- Log errors before raising when appropriate

```python
if not self._client.is_connected:
    raise RuntimeError("Not connected to Furby. Call connect() first.")
```

### Logging
- Use structured logging with `logger` from `logging` module
- Include relevant context in log messages
- Log levels: DEBUG (verbose), INFO (important events), WARNING (issues), ERROR (failures)

```python
logger.info(f"Connected to Furby at {address}")
logger.debug(f"Received notification: {data.hex()}")
```

## BLE Protocol Understanding

### Service UUID
- Main service: `dab91435-b5a1-e29c-b041-bcd562613bde`

### Key Characteristics
- **GeneralPlusWrite**: `dab91383-b5a1-e29c-b041-bcd562613bde` - Send commands
- **GeneralPlusListen**: `dab91382-b5a1-e29c-b041-bcd562613bde` - Receive responses/notifications
- **NordicWrite**: `dab90757-b5a1-e29c-b041-bcd562613bde` - Nordic commands (DLC transfer)
- **NordicListen**: `dab90756-b5a1-e29c-b041-bcd562613bde` - Nordic responses
- **FileWrite**: `dab90758-b5a1-e29c-b041-bcd562613bde` - DLC file data transfer

### Command Structure
Commands are byte arrays where the first byte is the command ID:
- `0x14`: Set antenna color (3 bytes: R, G, B)
- `0x13`: Trigger specific action (5 bytes: 0x00, input, index, subindex, specific)
- `0x24`: Set mood meter (4 bytes: 0x24, action, type, value)
- `0x50`: Announce DLC upload
- `0x60`: Load DLC, `0x61`: Activate DLC, `0x62`: Deactivate, `0x74`: Delete

### Action Hierarchy
Actions are organized as: **input** → **index** → **subindex** → **specific**
- Example: Input 1 (petting) → Index 0 → Subindex 0 → Specific 0-8 (variations)
- See `docs/actionlist.md` for complete list (1400+ actions with transcriptions)
- Web interface uses `web/actions.js` for searchable action database with 1400+ actions

## Web Interface Development

### UI Design Philosophy
- **Light & Colorful**: Pastel gradients (peach → pink → lavender)
- **Compact & Modern**: 25-40% reduced spacing from original dark theme
- **Sparkly Effects**: CSS animations with gradient shifts and glow
- **Glass Morphism**: Backdrop blur with semi-transparent cards

### Layout System
**CSS Grid for Alignment**
```css
.slider-group {
    display: grid;
    grid-template-columns: minmax(140px, max-content) 1fr auto;
    gap: 1rem;
}
```
- First column: Labels with consistent width (140px for mood, 70px for antenna)
- Second column: Flexible slider controls
- Third column: Auto-sized value displays

**Z-Index Management**
```
1-2:   .card elements (base layer)
100:   .action-helper (above cards)
9999:  .action-dropdown (topmost for visibility)
```
- Parent cards need `overflow: visible` for dropdowns to escape

### Interactive Elements

**Mood Sliders**
- Auto-update on `change` event (when released)
- Resend on 0/100 values when clicked and released (edge case handling)
- Status polling: GET `/status` every 10 seconds to sync UI
- Default values: Excitedness=50, Displeasedness=0, Tiredness=0, Fullness=50, Wellness=50

**Antenna Color Controls**
- Auto-send on `input` event (real-time updates while dragging)
- Clickable color preview to resend current color
- 8 preset colors + 5 memory slots + off/black
- Memory slots initialized with random bright colors (at least one RGB channel = 255)
- Recent colors stored in memory, not presets

**Custom Action Search**
- Dropdown with 1439+ actions from `actions.js`
- Search filters: category name, description text, coordinates
- Results limited to 50 for performance
- Recent actions (max 10) shown first with cookie persistence (365 days)
- Action description updates in real-time as input fields change
- Display format: `<strong>Category:</strong> description<br><small>Action: [i,x,s,p]</small>`

### Event Handling Patterns

**Real-time Updates (input event)**
```javascript
slider.addEventListener('input', () => {
    // Update preview/display immediately
    updatePreview();
});
```

**Final Value Updates (change event)**
```javascript
slider.addEventListener('change', () => {
    // Send to API when user releases control
    sendToFurby();
});
```

**Initialization on Page Load**
```javascript
// Initialize when DOM is ready
updateStatus();
setInterval(updateStatus, 10000);
updateColorMemoryDisplay(); // Apply random colors to memory buttons
```

### Cookie Management
```javascript
function setCookie(name, value, days = 365) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = name + "=" + JSON.stringify(value) + ";expires=" + date.toUTCString() + ";path=/";
}
```
- Recent actions: `furby_recent_actions` (10 items max, 365-day expiry)
- Could add color memory persistence in future

## FastAPI Endpoints

### REST API Patterns
- Use appropriate HTTP methods: GET (read), POST (create/action), DELETE (remove)
- Return Pydantic models for type safety
- Include proper HTTP status codes
- Use dependency injection for `FurbyConnect` instance

```python
@app.post("/antenna", response_model=dict)
async def set_antenna(color: AntennaColor, furby: FurbyConnect = Depends(get_furby)):
    """Set Furby's antenna LED color."""
    await furby.set_antenna_color(color.red, color.green, color.blue)
    return {"status": "success"}
```

### WebSocket Pattern
- Use for real-time sensor data streaming
- Send JSON messages with proper structure
- Handle connection lifecycle properly

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await furby.get_sensor_data()
            await websocket.send_json(data.model_dump())
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
```

## CLI Commands

### Typer Command Structure
- Use `typer.Typer()` app instance
- Rich formatting for output
- Handle async with `asyncio.run()`
- Provide helpful descriptions

```python
@app.command()
def antenna(
    red: int = typer.Option(..., help="Red value (0-255)"),
    green: int = typer.Option(..., help="Green value (0-255)"),
    blue: int = typer.Option(..., help="Blue value (0-255)"),
):
    """Set Furby's antenna LED color."""
    asyncio.run(set_antenna_async(red, green, blue))
```

## Testing Guidelines

### Test Structure
- Use `pytest` with async support (`pytest-asyncio`)
- Mock BLE operations with `unittest.mock`
- Test packet building without real hardware
- Use fixtures for common setup

```python
import pytest
from pyfluff.protocol import FurbyProtocol

def test_antenna_packet():
    packet = FurbyProtocol.set_antenna_color(255, 128, 0)
    assert packet == bytearray([0x14, 255, 128, 0])
```

## Documentation Standards

### Docstrings
- Use Google-style docstrings
- Document all public methods, classes, and modules
- Include parameter types and return types
- Provide usage examples for complex functions

```python
async def trigger_action(
    self, 
    input_id: int, 
    index: int = 0, 
    subindex: int = 0, 
    specific: int = 0
) -> None:
    """Trigger a specific Furby action sequence.
    
    Args:
        input_id: Top-level action category (0-75)
        index: Action index within input (default: 0)
        subindex: Action subindex (default: 0)
        specific: Specific variation (default: 0)
        
    Example:
        >>> await furby.trigger_action(1, 0, 0, 0)  # Petting reaction
    """
```

### Protocol Documentation
- All protocol details are in `docs/` directory
- Reference original bluefluff research with attribution
- Update docs when adding new protocol features

## Common Patterns

### Context Manager Usage
```python
async with FurbyConnect.discover() as furby:
    await furby.set_antenna_color(255, 0, 0)
    await furby.trigger_action(1, 0, 0, 0)
```

### Error Recovery
```python
try:
    async with asyncio.timeout(10):
        await furby.connect(address)
except asyncio.TimeoutError:
    logger.error("Connection timeout")
    raise RuntimeError("Failed to connect to Furby")
```

### DLC Upload with Progress
```python
dlc_manager = DLCManager(furby)
await dlc_manager.upload_dlc(
    file_path="custom.dlc",
    slot=0,
    progress_callback=lambda done, total: print(f"{done}/{total}")
)
```

## Important Notes

### Attribution
- Original protocol reverse engineering by Jeija (bluefluff project)
- Always credit original research when documenting protocol details
- See `docs/` for complete protocol documentation with attribution

### Platform Considerations
- Primary target: Raspberry Pi OS (Bookworm)
- BLE requires Linux with BlueZ stack or macOS
- Windows support via Bleak (with limitations)

### DLC File Handling
- DLC files are 20-byte chunks sent to FileWrite characteristic
- Upload takes 3-5 minutes depending on file size
- Must enable Nordic Packet ACK before upload
- Debug menu shows slot states: 0=empty, 1=uploading, 2=loaded, 3=active

### Safety Warnings
- Users can brick their Furby with custom DLC files
- Always include disclaimers about warranty void
- Educational purposes only

## Project-Specific Conventions

### File Organization
- Keep protocol logic in `protocol.py`
- BLE connection/communication in `furby.py`
- API routes in `server.py`
- CLI commands in `cli.py`
- Data models in `models.py`
- Web frontend in `web/` directory (HTML/CSS/JS)
- Utility scripts in `scripts/` directory

### Web Development Guidelines

**Action and Name Databases**
- `web/actions.js` contains 1400+ Furby actions with categories and descriptions
- `web/names.js` contains 129 Furby names with searchable dropdown functionality
- Both files include helper functions for cookies, search, and dropdown management

**CSS Layout Principles**
- Use CSS Grid with `minmax()` for aligned layouts
- Mood labels: `minmax(140px, max-content)`
- Antenna labels: `minmax(70px, max-content)`
- Set `overflow: visible` on parent cards for dropdown menus
- Z-index hierarchy: cards < helpers < dropdowns

**JavaScript Patterns**
- Use `addEventListener('input', ...)` for real-time updates
- Use `addEventListener('change', ...)` for final values
- Cookie storage for persistence: `setCookie(name, value, days)`
- Update description displays with `innerHTML` for rich formatting
- Show action coordinates with category: `<strong>Category:</strong> description<br><small>Action: [i,x,s,p]</small>`

**Color Memory System**
- Generate random bright colors: ensure at least one RGB channel = 255
- Initialize on page load: call `updateColorMemoryDisplay()` after DOM ready
- Store last 5 colors in memory slots
- Update buttons with `style.background = rgb(r,g,b)`

### Naming Conventions
- Classes: PascalCase (`FurbyConnect`, `DLCManager`)
- Functions/methods: snake_case (`set_antenna_color`, `trigger_action`)
- Constants: UPPER_SNAKE_CASE (`FURBY_SERVICE_UUID`)
- Private methods: `_underscore_prefix`
- CSS classes: kebab-case (`mood-controls`, `action-dropdown`)

### Import Order
1. Standard library
2. Third-party packages
3. Local modules

```python
import asyncio
from typing import Optional

from bleak import BleakClient, BleakScanner
from pydantic import BaseModel

from .protocol import FurbyProtocol
from .models import AntennaColor
```

## When Suggesting Code

1. **Always use type hints** - Every function needs proper typing
2. **Use async/await** - All BLE operations are asynchronous
3. **Include error handling** - Check connection state, handle timeouts
4. **Add docstrings** - Document public APIs with examples
5. **Follow Pydantic v2** - Use modern syntax (ConfigDict, Field)
6. **Reference protocol docs** - Link to relevant documentation in comments
7. **Test packet format** - Verify byte arrays match protocol specification
8. **Consider cross-platform** - Code should work on Pi, macOS, Linux

## Quick Reference

### Common Tasks

**Connect to Furby:**
```python
async with FurbyConnect.discover() as furby:
    # Work with furby
```

**Build command packet:**
```python
packet = FurbyProtocol.set_antenna_color(255, 0, 0)
await furby._write_gp(packet)
```

**Add new endpoint:**
```python
@app.post("/new-endpoint")
async def new_endpoint(
    data: MyModel,
    furby: FurbyConnect = Depends(get_furby)
) -> dict:
    await furby.some_command()
    return {"status": "success"}
```

**Add CLI command:**
```python
@app.command()
def new_command(arg: str = typer.Argument(..., help="Description")):
    """Command description."""
    asyncio.run(async_function(arg))
```

This document ensures consistent, high-quality code contributions to PyFluff!

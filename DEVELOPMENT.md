# PyFluff Development Guide

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyfluff --cov-report=html

# Run specific test file
pytest tests/test_protocol.py

# Run with verbose output
pytest -v
```

## Code Quality

```bash
# Type checking
mypy pyfluff/

# Linting
ruff check pyfluff/

# Formatting
black pyfluff/
```

## Running the Server

### Development mode (with auto-reload):
```bash
uvicorn pyfluff.server:app --reload --host 0.0.0.0 --port 8080
```

### Production mode:
```bash
python -m pyfluff.server
```

## Using the CLI

```bash
# Scan for Furby devices
pyfluff scan

# Get device info
pyfluff info

# Set antenna color
pyfluff antenna --red 255 --green 0 --blue 0

# Trigger action
pyfluff action --input 55 --index 2 --subindex 14 --specific 0

# Monitor sensors
pyfluff monitor --duration 30
```

## Project Structure

- `pyfluff/` - Main package
  - `furby.py` - Core Furby connection class
  - `protocol.py` - BLE protocol definitions
  - `models.py` - Pydantic data models
  - `commands.py` - Command handlers
  - `dlc.py` - DLC file management
  - `server.py` - FastAPI web server
  - `cli.py` - Command-line interface
- `web/` - Web interface files
- `examples/` - Example scripts
- `tests/` - Test suite

## Adding New Features

1. Define protocol constants in `protocol.py`
2. Add methods to `FurbyConnect` class in `furby.py`
3. Add API endpoints to `server.py`
4. Add CLI commands to `cli.py`
5. Write tests in `tests/`
6. Update documentation

## Bluetooth Debugging

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

View raw BLE packets in the logs to understand protocol better.

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests
4. Ensure all tests pass
5. Update documentation
6. Submit a pull request

## Troubleshooting

### Bluetooth not found
- Ensure Bluetooth is enabled: `sudo systemctl start bluetooth`
- Check adapter: `hciconfig`
- Unblock: `rfkill unblock bluetooth`

### Permission denied
- Add user to bluetooth group: `sudo usermod -a -G bluetooth $USER`
- Or run with sudo (not recommended)

### Connection fails
- Ensure Furby is powered on
- Make sure Furby is not connected to the mobile app
- Try moving closer to Furby
- Restart Bluetooth: `sudo systemctl restart bluetooth`

### Package import errors
- Reinstall in development mode: `pip install -e .`
- Check virtual environment is activated

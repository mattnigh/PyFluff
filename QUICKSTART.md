# PyFluff Quick Start Guide

## Installation (5 minutes)

### On Raspberry Pi OS (Bookworm)

```bash
# Clone the repository
git clone <repository-url> PyFluff
cd PyFluff

# Run installation script
./install.sh

# Activate virtual environment
source venv/bin/activate
```

### Manual Installation

```bash
# Install system dependencies
sudo apt update
sudo apt install python3.11 python3-pip python3-venv bluetooth bluez

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install PyFluff
pip install -r requirements.txt
pip install -e .
```

## Quick Usage

### 1. Start Web Server (Easiest)

```bash
source venv/bin/activate
python -m pyfluff.server
```

Then open http://localhost:8080 in your browser.

### 2. Command Line

```bash
# Scan for Furby
pyfluff scan

# Get device info
pyfluff info

# Set antenna to red
pyfluff antenna --red 255 --green 0 --blue 0

# Make Furby giggle
pyfluff action --input 55 --index 2 --subindex 14 --specific 0

# Monitor sensors for 30 seconds
pyfluff monitor --duration 30
```

### 3. Python Script

Create `my_furby.py`:

```python
import asyncio
from pyfluff import FurbyConnect

async def main():
    # Connect to Furby
    async with FurbyConnect() as furby:
        print("Connected!")
        
        # Set antenna to blue
        await furby.set_antenna_color(0, 0, 255)
        
        # Wait a bit
        await asyncio.sleep(2)
        
        # Make Furby giggle
        await furby.trigger_action(55, 2, 14, 0)

asyncio.run(main())
```

Run it:
```bash
python my_furby.py
```

## Common Actions

### Antenna Colors
- Red: `pyfluff antenna --red 255 --green 0 --blue 0`
- Green: `pyfluff antenna --red 0 --green 255 --blue 0`
- Blue: `pyfluff antenna --red 0 --green 0 --blue 255`
- Off: `pyfluff antenna --red 0 --green 0 --blue 0`

### Fun Actions
- Giggle: `--input 55 --index 2 --subindex 14 --specific 0`
- Puke: `--input 56 --index 3 --subindex 15 --specific 1`

### Debug Menu
```bash
pyfluff debug
```
Press multiple times to cycle through:
1. Furby mood display
2. RTC and BLE overview
3. Accelerometer
4. Microphone
5. Furby-to-Furby (F2F)
6. DLC slots
7. Notification timings

## Troubleshooting

### "No Furby devices found"
1. Make sure Furby is turned on
2. Close the Furby Connect app if open
3. Move closer to Furby
4. Try: `sudo systemctl restart bluetooth`

### "Permission denied"
Add yourself to bluetooth group:
```bash
sudo usermod -a -G bluetooth $USER
# Log out and back in
```

### "Module not found"
Make sure virtual environment is activated:
```bash
source venv/bin/activate
```

### Bluetooth not working
```bash
# Check status
sudo systemctl status bluetooth

# Restart
sudo systemctl restart bluetooth

# Unblock
sudo rfkill unblock bluetooth
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [examples/](examples/) for more code samples
- See [DEVELOPMENT.md](DEVELOPMENT.md) for development setup
- Browse API docs at http://localhost:8080/docs

## Getting Help

1. Check the original [bluefluff documentation](https://github.com/Jeija/bluefluff)
2. Read the protocol documentation in the `doc/` folder
3. Look at the example scripts in `examples/`
4. Check the test files in `tests/` for usage examples

## Safety Reminder

⚠️ **This software is for educational purposes only.**

- You may void your warranty
- You could potentially brick your Furby
- Use at your own risk
- Always test with caution

Have fun exploring Furby Connect! 🐾

#!/bin/bash
# PyFluff Installation Script for Raspberry Pi OS (Bookworm)

set -e

echo "======================================"
echo "PyFluff Installation Script"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    echo "Error: Python 3.11 or later is required (found $PYTHON_VERSION)"
    echo "Please upgrade Python before continuing."
    exit 1
fi

echo "✓ Python $PYTHON_VERSION found"

# Check for bluetooth
echo ""
echo "Checking Bluetooth..."
if ! command -v bluetoothctl &> /dev/null; then
    echo "Warning: bluetoothctl not found. Installing bluez..."
    sudo apt update
    sudo apt install -y bluetooth bluez
fi

echo "✓ Bluetooth tools available"

# Enable and start bluetooth service
echo ""
echo "Enabling Bluetooth service..."
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
sudo rfkill unblock bluetooth

echo "✓ Bluetooth service enabled"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

echo "✓ Virtual environment created"

# Activate virtual environment and install dependencies
echo ""
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Dependencies installed"

# Install in development mode
echo ""
echo "Installing PyFluff..."
pip install -e .

echo "✓ PyFluff installed"

# Test installation
echo ""
echo "Testing installation..."
python -c "import pyfluff; print(f'PyFluff version {pyfluff.__version__} imported successfully')"

echo ""
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""
echo "To use PyFluff:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the web server:"
echo "   python -m pyfluff.server"
echo ""
echo "3. Use the CLI:"
echo "   pyfluff scan"
echo "   pyfluff --help"
echo ""
echo "4. Open web interface:"
echo "   http://localhost:8080"
echo ""
echo "For more information, see README.md"
echo ""

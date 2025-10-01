#!/usr/bin/env python3
"""
Quick test script to verify Furby connection and command sending.
Run this to debug if the web UI isn't working.
"""

import asyncio
import logging
from pyfluff.furby import FurbyConnect

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

async def test_connection():
    """Test basic Furby connection and commands."""
    print("=" * 60)
    print("PyFluff Connection Test")
    print("=" * 60)
    
    print("\n1. Discovering Furby devices...")
    devices = await FurbyConnect.discover(timeout=5.0)
    
    if not devices:
        print("❌ No Furby devices found!")
        print("Make sure:")
        print("  - Furby is powered on")
        print("  - Furby is in range")
        print("  - Bluetooth is enabled on your Mac")
        return
    
    print(f"✓ Found {len(devices)} Furby device(s):")
    for device in devices:
        print(f"  - {device.name} ({device.address})")
    
    print("\n2. Connecting to Furby...")
    furby = FurbyConnect(device=devices[0])
    
    try:
        await furby.connect(timeout=10.0)
        print("✓ Connected successfully!")
        
        print("\n3. Testing commands...")
        
        # Test antenna color
        print("  - Setting antenna to RED...")
        await furby.set_antenna_color(255, 0, 0)
        await asyncio.sleep(1)
        
        print("  - Setting antenna to GREEN...")
        await furby.set_antenna_color(0, 255, 0)
        await asyncio.sleep(1)
        
        print("  - Setting antenna to BLUE...")
        await furby.set_antenna_color(0, 0, 255)
        await asyncio.sleep(1)
        
        print("  - Turning antenna OFF...")
        await furby.set_antenna_color(0, 0, 0)
        await asyncio.sleep(1)
        
        # Test LCD
        print("  - Turning LCD ON...")
        await furby.set_lcd_backlight(True)
        await asyncio.sleep(2)
        
        print("  - Turning LCD OFF...")
        await furby.set_lcd_backlight(False)
        await asyncio.sleep(1)
        
        # Test action
        print("  - Triggering action (giggle)...")
        await furby.trigger_action(55, 2, 14, 0)
        await asyncio.sleep(3)
        
        print("\n✓ All tests passed!")
        print("\nIf this works but the web UI doesn't, the issue is in the")
        print("web server or JavaScript code, not the BLE communication.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n4. Disconnecting...")
        await furby.disconnect()
        print("✓ Disconnected")

if __name__ == "__main__":
    asyncio.run(test_connection())

"""
Basic control example for PyFluff.

This example demonstrates how to connect to Furby and perform basic operations.
"""

import asyncio
import logging

from pyfluff.furby import FurbyConnect

# Enable logging to see what's happening
logging.basicConfig(level=logging.INFO)


async def main() -> None:
    """Main function demonstrating basic Furby control."""

    # Use context manager for automatic connection/disconnection
    async with FurbyConnect() as furby:
        print("Connected to Furby!")

        # Get device information
        info = await furby.get_device_info()
        print(f"\nDevice Information:")
        print(f"  Manufacturer: {info.manufacturer}")
        print(f"  Model: {info.model_number}")
        print(f"  Firmware: {info.firmware_revision}")

        # Set antenna color to red
        print("\nSetting antenna to red...")
        await furby.set_antenna_color(255, 0, 0)
        await asyncio.sleep(2)

        # Set antenna color to green
        print("Setting antenna to green...")
        await furby.set_antenna_color(0, 255, 0)
        await asyncio.sleep(2)

        # Set antenna color to blue
        print("Setting antenna to blue...")
        await furby.set_antenna_color(0, 0, 255)
        await asyncio.sleep(2)

        # Turn off antenna
        print("Turning off antenna...")
        await furby.set_antenna_color(0, 0, 0)

        # Control LCD backlight
        print("\nTurning LCD off...")
        await furby.set_lcd_backlight(False)
        await asyncio.sleep(2)

        print("Turning LCD on...")
        await furby.set_lcd_backlight(True)

        # Trigger an action (giggle)
        print("\nMaking Furby giggle...")
        await furby.trigger_action(input=55, index=2, subindex=14, specific=0)
        await asyncio.sleep(3)

        print("\nExample complete!")


if __name__ == "__main__":
    asyncio.run(main())

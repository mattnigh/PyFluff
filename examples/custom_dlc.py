"""
Custom DLC example for PyFluff.

This example shows how to upload and activate custom DLC files.
"""

import asyncio
import logging
from pathlib import Path

from pyfluff.furby import FurbyConnect
from pyfluff.dlc import DLCManager

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    """Demonstrate DLC management."""

    async with FurbyConnect() as furby:
        print("Connected to Furby!")

        # Create DLC manager
        dlc_manager = DLCManager(furby)

        # Example: Upload a DLC file
        # You would need an actual DLC file for this to work
        dlc_file = Path("path/to/your/dlc_file.DLC")

        if dlc_file.exists():
            print(f"\nUploading {dlc_file.name}...")
            await dlc_manager.upload_dlc(dlc_file, slot=2)
            print("Upload complete!")

            print("\nLoading DLC from slot 2...")
            await dlc_manager.load_dlc(slot=2)

            print("Activating DLC...")
            await dlc_manager.activate_dlc()

            print("\nDLC is now active on Furby!")

            # Wait a bit to see the effects
            await asyncio.sleep(10)

            # Deactivate when done
            print("\nDeactivating DLC...")
            await dlc_manager.deactivate_dlc(slot=2)

        else:
            print(f"\nDLC file not found: {dlc_file}")
            print("This is just an example. Replace the path with an actual DLC file.")

            # Show other DLC operations
            print("\nYou can also:")
            print("  - Delete a DLC: await dlc_manager.delete_dlc(slot=2)")
            print("  - Load a DLC: await dlc_manager.load_dlc(slot=2)")
            print("  - Activate: await dlc_manager.activate_dlc()")
            print("  - Deactivate: await dlc_manager.deactivate_dlc(slot=2)")


if __name__ == "__main__":
    asyncio.run(main())

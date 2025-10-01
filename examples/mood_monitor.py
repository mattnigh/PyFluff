"""
Mood monitoring example for PyFluff.

This example demonstrates how to manipulate Furby's emotional state.
"""

import asyncio
import logging

from pyfluff.furby import FurbyConnect
from pyfluff.protocol import MoodMeterType

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    """Demonstrate mood control."""

    async with FurbyConnect() as furby:
        print("Connected to Furby!")
        print("\nManipulating Furby's mood...\n")

        # Make Furby very happy
        print("Making Furby excited...")
        await furby.set_mood(MoodMeterType.EXCITEDNESS, 100, set_absolute=True)
        await asyncio.sleep(2)

        # Make Furby full
        print("Making Furby full...")
        await furby.set_mood(MoodMeterType.FULLNESS, 100, set_absolute=True)
        await asyncio.sleep(2)

        # Make Furby healthy
        print("Making Furby healthy...")
        await furby.set_mood(MoodMeterType.WELLNESS, 100, set_absolute=True)
        await asyncio.sleep(2)

        # Make Furby tired
        print("Making Furby tired...")
        await furby.set_mood(MoodMeterType.TIREDNESS, 80, set_absolute=True)
        await asyncio.sleep(2)

        # Reset everything to neutral
        print("\nResetting to neutral mood...")
        await furby.set_mood(MoodMeterType.EXCITEDNESS, 50, set_absolute=True)
        await furby.set_mood(MoodMeterType.FULLNESS, 50, set_absolute=True)
        await furby.set_mood(MoodMeterType.WELLNESS, 50, set_absolute=True)
        await furby.set_mood(MoodMeterType.TIREDNESS, 50, set_absolute=True)
        await furby.set_mood(MoodMeterType.DISPLEASEDNESS, 0, set_absolute=True)

        print("\nMood manipulation complete!")


if __name__ == "__main__":
    asyncio.run(main())

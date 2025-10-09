#!/usr/bin/env python3
"""
Example: Triggering a sequence of Furby actions.

This example demonstrates how to send multiple actions to Furby that execute
one after another with configurable delays between them.
"""

import asyncio
import httpx


async def play_action_sequence():
    """Play a sequence of Furby actions using the REST API."""
    
    base_url = "http://localhost:8080"
    
    # Define a sequence of actions to play
    # Example: Make Furby sing multiple notes from the octave
    action_sequence = {
        "actions": [
            {"input": 71, "index": 0, "subindex": 0, "specific": 0},  # Do
            {"input": 71, "index": 0, "subindex": 0, "specific": 1},  # Re
            {"input": 71, "index": 0, "subindex": 0, "specific": 2},  # Mi
            {"input": 71, "index": 0, "subindex": 0, "specific": 3},  # Fa
            {"input": 71, "index": 0, "subindex": 0, "specific": 4},  # Sol
            {"input": 71, "index": 0, "subindex": 0, "specific": 5},  # La
            {"input": 71, "index": 0, "subindex": 0, "specific": 6},  # Ti
            {"input": 71, "index": 0, "subindex": 0, "specific": 7},  # Do
        ],
        "delay": 1.5  # Wait 1.5 seconds between each note
    }
    
    async with httpx.AsyncClient() as client:
        print("Connecting to Furby...")
        # First connect to Furby
        await client.post(f"{base_url}/connect")
        print("Connected!")
        
        print(f"\nPlaying sequence of {len(action_sequence['actions'])} actions...")
        print(f"Delay between actions: {action_sequence['delay']} seconds")
        
        # Trigger the action sequence
        response = await client.post(
            f"{base_url}/actions/sequence",
            json=action_sequence,
            timeout=60.0  # Allow time for the full sequence
        )
        
        result = response.json()
        print(f"\n✓ {result['message']}")
        print(f"  Actions executed: {result['data']['actions_executed']}")
        
        # Optional: Disconnect when done
        # await client.post(f"{base_url}/disconnect")


async def play_custom_sequence():
    """Play a custom action sequence - feel free to modify!"""
    
    base_url = "http://localhost:8080"
    
    # Create your own sequence here!
    my_sequence = {
        "actions": [
            {"input": 55, "index": 2, "subindex": 14, "specific": 0},  # Giggle
            {"input": 17, "index": 0, "subindex": 0, "specific": 0},   # Sing song 1
            {"input": 56, "index": 3, "subindex": 15, "specific": 1},  # Puke
        ],
        "delay": 3.0  # Wait 3 seconds between actions
    }
    
    async with httpx.AsyncClient() as client:
        print("Connecting to Furby...")
        await client.post(f"{base_url}/connect")
        print("Connected!")
        
        print(f"\nPlaying custom sequence...")
        response = await client.post(
            f"{base_url}/actions/sequence",
            json=my_sequence,
            timeout=60.0
        )
        
        result = response.json()
        print(f"\n✓ {result['message']}")


if __name__ == "__main__":
    print("PyFluff Action Sequence Example")
    print("=" * 50)
    print("\n1. Musical scale (Do-Re-Mi-Fa-Sol-La-Ti-Do)")
    print("2. Custom sequence (Giggle, Sing, Puke)")
    
    choice = input("\nSelect example (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(play_action_sequence())
    elif choice == "2":
        asyncio.run(play_custom_sequence())
    else:
        print("Invalid choice. Please run again and select 1 or 2.")

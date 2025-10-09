#!/usr/bin/env python3
"""
Make Furby sing by triggering a sequence of actions.

This script uses the action sequence API to send musical notes (71,0,0,0 through 71,0,0,7)
to make Furby sing the octave scale: Do-Re-Mi-Fa-Sol-La-Ti-Do
"""

import sys
import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()

# Server configuration
SERVER_URL = "http://localhost:8080"


def check_server() -> bool:
    """Check if the server is running and connected."""
    try:
        response = requests.get(f"{SERVER_URL}/status", timeout=2)
        if response.status_code == 200:
            status = response.json()
            if status['connected']:
                return True
            else:
                console.print("[red]Server is running but not connected to Furby.[/red]")
                console.print("Please connect via the web UI first: http://localhost:8080")
                return False
        else:
            console.print(f"[red]Server returned status {response.status_code}[/red]")
            return False
    except requests.exceptions.ConnectionError:
        console.print("[red]Cannot connect to PyFluff server.[/red]")
        console.print("Make sure the server is running:")
        console.print("  [cyan]python -m pyfluff.server[/cyan]")
        return False
    except Exception as e:
        console.print(f"[red]Error checking server: {e}[/red]")
        return False


def send_sequence() -> bool:
    """Send the singing sequence to Furby using the action sequence API."""
    # Build the sequence of musical notes: Do-Re-Mi-Fa-Sol-La-Ti-Do
    notes = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Ti", "Do"]
    
    sequence = {
        "actions": [
            {"input": 71, "index": 0, "subindex": 0, "specific": i}
            for i in range(8)
        ],
        "delay": 3  # 3 seconds between each note
    }
    
    console.print("[bold cyan]🎵 Making Furby Sing the Octave Scale! 🎵[/bold cyan]")
    console.print(f"Notes: {' - '.join(notes)}\n")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task(
                "Sending sequence to Furby...",
                total=100
            )
            
            response = requests.post(
                f"{SERVER_URL}/actions/sequence",
                json=sequence,
                timeout=30  # Allow time for the full sequence
            )
            
            progress.update(task, completed=50)
            
            if response.status_code == 200:
                result = response.json()
                progress.update(task, completed=100)
                
                console.print(f"\n[green]✓[/green] {result['message']}")
                console.print(f"  Actions executed: {result['data']['actions_executed']}")
                console.print(f"  Delay between notes: {result['data']['delay_used']}s")
                return True
            else:
                error = response.json().get('detail', 'Unknown error')
                console.print(f"\n[red]✗ Sequence failed: {error}[/red]")
                return False
                
    except requests.exceptions.Timeout:
        console.print("\n[red]✗ Request timed out - sequence may still be running[/red]")
        return False
    except Exception as e:
        console.print(f"\n[red]✗ Error sending sequence: {e}[/red]")
        return False


def sing() -> int:
    """Execute the singing sequence."""
    # Check server connection
    if not check_server():
        return 1
    
    console.print("[green]✓[/green] Server connected\n")
    
    # Send the sequence
    if send_sequence():
        console.print("\n[bold green]🎉 Furby finished singing! 🎉[/bold green]")
        return 0
    else:
        return 1


def main():
    """Main entry point."""
    try:
        result = sing()
        sys.exit(result)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()

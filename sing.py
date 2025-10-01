#!/usr/bin/env python3
"""
Make Furby sing by triggering a sequence of actions.

This script sends actions 71,0,0,0 through 71,0,0,7 to the PyFluff server,
waiting 1 second between each action.
"""

import asyncio
import sys
import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

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


def send_action(input_val: int, index: int, subindex: int, specific: int) -> bool:
    """Send an action to the Furby via the API."""
    try:
        response = requests.post(
            f"{SERVER_URL}/action",
            json={
                "input": input_val,
                "index": index,
                "subindex": subindex,
                "specific": specific
            },
            timeout=5
        )
        
        if response.status_code == 200:
            return True
        else:
            error = response.json().get('detail', 'Unknown error')
            console.print(f"[red]Action failed: {error}[/red]")
            return False
            
    except Exception as e:
        console.print(f"[red]Error sending action: {e}[/red]")
        return False


async def sing():
    """Execute the singing sequence."""
    console.print("[bold cyan]🎵 Making Furby Sing! 🎵[/bold cyan]\n")
    
    # Check server connection
    if not check_server():
        return 1
    
    console.print("[green]✓[/green] Server connected\n")
    
    # Execute actions 71,0,0,0 through 71,0,0,7
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        for specific in range(8):
            task = progress.add_task(
                f"Sending action 71,0,0,{specific}...",
                total=1
            )
            
            success = send_action(71, 0, 0, specific)
            
            if success:
                progress.update(task, completed=1)
                console.print(f"[green]✓[/green] Action 71,0,0,{specific} sent")
            else:
                progress.update(task, completed=1)
                console.print(f"[red]✗[/red] Action 71,0,0,{specific} failed")
                return 1
            
            # Wait 1 second before next action (except after the last one)
            if specific < 7:
                await asyncio.sleep(2)
    
    console.print("\n[bold green]🎉 Singing sequence complete! 🎉[/bold green]")
    return 0


def main():
    """Main entry point."""
    try:
        result = asyncio.run(sing())
        sys.exit(result)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()

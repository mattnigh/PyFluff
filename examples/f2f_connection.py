"""
F2F Mode Connection Example

This example demonstrates how to connect to a Furby that's in F2F
(Furby-to-Furby) communication mode by using its MAC address directly.

When Furbies are communicating with each other, they may stop advertising
their BLE presence, making them invisible to standard discovery scans.
Direct connection by MAC address bypasses discovery.

Usage:
    python examples/f2f_connection.py AA:BB:CC:DD:EE:FF
"""

import asyncio
import sys
from rich.console import Console
from rich.panel import Panel

from pyfluff.furby import FurbyConnect

console = Console()


async def connect_by_address(address: str) -> None:
    """
    Connect to a Furby by its MAC address.
    
    Args:
        address: MAC address in format AA:BB:CC:DD:EE:FF
    """
    console.print(Panel(
        f"[cyan]Connecting to Furby at:[/cyan] [bold]{address}[/bold]\n"
        "[dim]Using enhanced connection with multiple retries...[/dim]\n"
        "[dim]This will work even if Furby is in F2F mode![/dim]",
        title="F2F Mode Connection",
        border_style="magenta"
    ))
    
    furby = FurbyConnect()
    
    try:
        # Connect directly by MAC address with retries (bypasses discovery)
        console.print("[yellow]Initiating connection with 5 retries...[/yellow]")
        await furby.connect(address=address, timeout=15.0, retries=5)
        
        console.print("[green]✓ Connected successfully![/green]\n")
        
        # Get device info
        console.print("[cyan]Fetching device information...[/cyan]")
        info = await furby.get_device_info()
        
        console.print(Panel(
            f"[cyan]Manufacturer:[/cyan] {info.manufacturer or 'N/A'}\n"
            f"[cyan]Model:[/cyan] {info.model_number or 'N/A'}\n"
            f"[cyan]Serial:[/cyan] {info.serial_number or 'N/A'}\n"
            f"[cyan]Firmware:[/cyan] {info.firmware_revision or 'N/A'}",
            title="Device Info",
            border_style="green"
        ))
        
        # Test control by flashing the antenna
        console.print("\n[yellow]Testing control by cycling antenna colors...[/yellow]")
        
        colors = [
            (255, 0, 0, "Red"),
            (0, 255, 0, "Green"),
            (0, 0, 255, "Blue"),
            (255, 255, 0, "Yellow"),
            (255, 0, 255, "Magenta"),
        ]
        
        for r, g, b, name in colors:
            console.print(f"  Setting antenna to [bold]{name}[/bold]...")
            await furby.set_antenna_color(r, g, b)
            await asyncio.sleep(1)
        
        # Turn off antenna
        console.print("  Turning antenna off...")
        await furby.set_antenna_color(0, 0, 0)
        
        console.print("\n[green]✓ Control test successful![/green]")
        console.print("[dim]Furby is responding to commands despite being in F2F mode.[/dim]")
        
        # Disconnect
        await furby.disconnect()
        console.print("\n[cyan]Disconnected from Furby[/cyan]")
        
    except Exception as e:
        console.print(f"\n[red]✗ Connection failed:[/red] {e}\n")
        console.print(Panel(
            "[yellow]Troubleshooting tips:[/yellow]\n\n"
            "1. Verify MAC address format: AA:BB:CC:DD:EE:FF\n"
            "2. Ensure Furby is powered on and within range\n"
            "3. Try waking Furby by touching its sensors\n"
            "4. Separate Furbies if they're actively in F2F mode\n"
            "5. Wait 30-60 seconds after waking before connecting\n"
            "6. Check Bluetooth is enabled on your system\n"
            "7. Use 'pyfluff scan --all' to verify MAC address\n"
            "8. Try increasing retries: --retries 10 --timeout 20",
            title="Connection Failed",
            border_style="red"
        ))
        sys.exit(1)


async def demo_discovery_vs_direct() -> None:
    """Demonstrate the difference between discovery and direct connection."""
    console.print(Panel(
        "[bold cyan]F2F Mode Connection Demo[/bold cyan]\n\n"
        "This example demonstrates two connection methods:\n\n"
        "[green]1. Discovery (may fail in F2F mode)[/green]\n"
        "   Scans for advertising Furbies, which may not work\n"
        "   if the Furby is actively communicating with another Furby.\n\n"
        "[yellow]2. Direct connection (works in F2F mode)[/yellow]\n"
        "   Connects directly by MAC address, bypassing discovery.\n"
        "   This works even when Furby stops advertising.",
        title="Connection Methods",
        border_style="magenta"
    ))
    
    console.print("\n[cyan]Method 1: Discovery-based connection[/cyan]")
    console.print("[dim]Scanning for advertising Furbies...[/dim]")
    
    try:
        devices = await FurbyConnect.discover(timeout=5.0)
        if devices:
            console.print(f"[green]✓ Found {len(devices)} Furby device(s)[/green]")
            for device in devices:
                console.print(f"  • {device.name} at {device.address}")
        else:
            console.print("[yellow]⚠ No Furbies found (possibly in F2F mode)[/yellow]")
    except Exception as e:
        console.print(f"[red]✗ Discovery failed: {e}[/red]")
    
    console.print("\n[cyan]Method 2: Direct connection by MAC address[/cyan]")
    console.print("[dim]Requires knowing the Furby's MAC address in advance[/dim]")
    console.print("[green]✓ This method works even in F2F mode![/green]")
    console.print("\n[bold]Usage:[/bold]")
    console.print("  python examples/f2f_connection.py AA:BB:CC:DD:EE:FF")


def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2:
        console.print("[yellow]No MAC address provided. Showing demo...[/yellow]\n")
        asyncio.run(demo_discovery_vs_direct())
        console.print("\n[bold cyan]To connect to your Furby:[/bold cyan]")
        console.print("  python examples/f2f_connection.py [bold]YOUR_MAC_ADDRESS[/bold]")
        console.print("\n[dim]Tip: Find your Furby's MAC address with:[/dim]")
        console.print("  python -m pyfluff.cli scan")
        sys.exit(0)
    
    address = sys.argv[1]
    
    # Validate MAC address format (basic check)
    if len(address) != 17 or address.count(':') != 5:
        console.print(f"[red]Invalid MAC address format:[/red] {address}")
        console.print("[yellow]Expected format:[/yellow] AA:BB:CC:DD:EE:FF")
        sys.exit(1)
    
    asyncio.run(connect_by_address(address))


if __name__ == "__main__":
    main()

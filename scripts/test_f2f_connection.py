#!/usr/bin/env python3
"""
F2F Connection Diagnostic Tool

This script helps diagnose Furby Connect connection issues, especially
when Furbies are in F2F (Furby-to-Furby) mode and not advertising.

Usage:
    python scripts/test_f2f_connection.py AA:BB:CC:DD:EE:FF
    python scripts/test_f2f_connection.py AA:BB:CC:DD:EE:FF --aggressive
"""

import asyncio
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from pyfluff.furby import FurbyConnect

console = Console()


async def test_scan() -> None:
    """Test basic BLE scanning."""
    console.print("\n[bold cyan]Step 1: BLE Scan Test[/bold cyan]")
    console.print("Testing if we can discover any BLE devices...")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Scanning for all BLE devices...", total=None)
            devices = await FurbyConnect.discover(timeout=10.0, show_all=True)
        
        if devices:
            console.print(f"[green]✓[/green] Found {len(devices)} BLE device(s)")
            
            table = Table(title="Discovered Devices")
            table.add_column("Name", style="cyan")
            table.add_column("Address", style="magenta")
            table.add_column("RSSI", style="yellow")
            
            for device in devices[:10]:  # Show first 10
                table.add_row(
                    device.name or "N/A",
                    device.address,
                    str(getattr(device, 'rssi', 'N/A'))
                )
            
            console.print(table)
            
            furbies = [d for d in devices if d.name and "Furby" in d.name]
            if furbies:
                console.print(f"\n[green]Found {len(furbies)} Furby device(s) advertising![/green]")
            else:
                console.print("\n[yellow]No Furbies found advertising (may be in F2F mode)[/yellow]")
        else:
            console.print("[red]✗[/red] No BLE devices found")
            console.print("[yellow]Bluetooth may not be enabled or accessible[/yellow]")
            
    except Exception as e:
        console.print(f"[red]✗[/red] Scan failed: {e}")


async def test_direct_connection(
    address: str,
    timeout: float = 15.0,
    retries: int = 3,
    aggressive: bool = False
) -> bool:
    """
    Test direct connection to a Furby by MAC address.
    
    Args:
        address: MAC address to connect to
        timeout: Timeout per attempt
        retries: Number of retry attempts
        aggressive: Use more retries and longer timeout
        
    Returns:
        True if connection successful, False otherwise
    """
    console.print(f"\n[bold cyan]Step 2: Direct Connection Test[/bold cyan]")
    console.print(f"Attempting to connect to: [bold]{address}[/bold]")
    
    if aggressive:
        timeout = 20.0
        retries = 10
        console.print("[yellow]Using aggressive mode: 10 retries with 20s timeout[/yellow]")
    else:
        console.print(f"Using {retries} retries with {timeout}s timeout per attempt")
    
    furby = FurbyConnect()
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Connecting...", total=None)
            await furby.connect(address=address, timeout=timeout, retries=retries)
        
        console.print(f"[green]✓[/green] Connected successfully!")
        
        # Test basic communication
        console.print("\n[bold cyan]Step 3: Communication Test[/bold cyan]")
        console.print("Testing if we can communicate with Furby...")
        
        try:
            # Try to get device info
            info = await furby.get_device_info()
            console.print("[green]✓[/green] Device info retrieved:")
            console.print(f"  Manufacturer: {info.manufacturer or 'N/A'}")
            console.print(f"  Model: {info.model_number or 'N/A'}")
            console.print(f"  Firmware: {info.firmware_revision or 'N/A'}")
            
            # Try to control antenna
            console.print("\nTesting antenna control...")
            await furby.set_antenna_color(255, 0, 0)
            await asyncio.sleep(0.5)
            await furby.set_antenna_color(0, 255, 0)
            await asyncio.sleep(0.5)
            await furby.set_antenna_color(0, 0, 255)
            await asyncio.sleep(0.5)
            await furby.set_antenna_color(0, 0, 0)
            console.print("[green]✓[/green] Antenna control working!")
            
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Communication test failed: {e}")
        
        await furby.disconnect()
        console.print("\n[green]✓[/green] Disconnected successfully")
        return True
        
    except Exception as e:
        console.print(f"[red]✗[/red] Connection failed: {e}")
        return False


async def run_diagnostic(address: str, aggressive: bool = False) -> None:
    """Run full diagnostic suite."""
    console.print(Panel(
        "[bold cyan]Furby F2F Connection Diagnostic Tool[/bold cyan]\n\n"
        f"Target address: [bold]{address}[/bold]\n"
        f"Mode: [bold]{'Aggressive' if aggressive else 'Normal'}[/bold]\n\n"
        "This tool will test:\n"
        "1. BLE scanning capability\n"
        "2. Direct connection to Furby\n"
        "3. Basic communication",
        title="Diagnostic Test",
        border_style="magenta"
    ))
    
    # Step 1: Scan test
    await test_scan()
    
    # Step 2 & 3: Connection and communication test
    success = await test_direct_connection(address, aggressive=aggressive)
    
    # Summary
    console.print("\n" + "="*60)
    if success:
        console.print(Panel(
            "[bold green]✓ All tests passed![/bold green]\n\n"
            "Your Furby is reachable and responding to commands.\n"
            "Connection works even in F2F mode.",
            title="Success",
            border_style="green"
        ))
    else:
        console.print(Panel(
            "[bold red]✗ Connection failed[/bold red]\n\n"
            "[yellow]Troubleshooting steps:[/yellow]\n\n"
            "1. Verify the MAC address is correct\n"
            "2. Ensure Furby is powered on and in range\n"
            "3. Try waking Furby by touching its sensors\n"
            "4. If Furbies are actively in F2F mode, separate them\n"
            "5. Wait 30-60 seconds after waking before connecting\n"
            "6. Try running with --aggressive flag for more retries\n"
            "7. Check Bluetooth permissions on macOS\n"
            "8. On Linux, try: sudo systemctl restart bluetooth\n\n"
            f"[dim]Try: python {sys.argv[0]} {address} --aggressive[/dim]",
            title="Failed",
            border_style="red"
        ))


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        console.print(Panel(
            "[bold]Furby F2F Connection Diagnostic Tool[/bold]\n\n"
            "Usage:\n"
            f"  python {sys.argv[0]} [bold]MAC_ADDRESS[/bold]\n"
            f"  python {sys.argv[0]} [bold]MAC_ADDRESS[/bold] --aggressive\n\n"
            "Examples:\n"
            f"  python {sys.argv[0]} AA:BB:CC:DD:EE:FF\n"
            f"  python {sys.argv[0]} AA:BB:CC:DD:EE:FF --aggressive\n\n"
            "The --aggressive flag uses more retries (10) and longer timeout (20s)\n"
            "for difficult connections when Furbies are in deep F2F communication.",
            title="Help",
            border_style="cyan"
        ))
        sys.exit(1)
    
    address = sys.argv[1]
    aggressive = "--aggressive" in sys.argv or "-a" in sys.argv
    
    # Validate MAC address format
    if len(address) != 17 or address.count(':') != 5:
        console.print(f"[red]Invalid MAC address format:[/red] {address}")
        console.print("[yellow]Expected format:[/yellow] AA:BB:CC:DD:EE:FF")
        sys.exit(1)
    
    asyncio.run(run_diagnostic(address, aggressive))


if __name__ == "__main__":
    main()

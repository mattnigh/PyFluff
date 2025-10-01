"""
Command-line interface for PyFluff.

Provides a CLI for controlling Furby Connect from the terminal.
"""

import asyncio
import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel

from pyfluff.furby import FurbyConnect
from pyfluff.dlc import DLCManager

app = typer.Typer(help="PyFluff - Control Furby Connect from the command line")
console = Console()

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Less verbose for CLI
    format="%(message)s",
)


@app.command()
def scan(timeout: float = 10.0) -> None:
    """Scan for nearby Furby devices."""

    async def _scan() -> None:
        with console.status("[bold green]Scanning for Furby devices..."):
            devices = await FurbyConnect.discover(timeout=timeout)

        if not devices:
            console.print("[red]No Furby devices found[/red]")
            return

        table = Table(title="Found Furby Devices")
        table.add_column("Name", style="cyan")
        table.add_column("Address", style="magenta")
        table.add_column("RSSI", style="green")

        for device in devices:
            table.add_row(
                device.name or "Unknown",
                device.address,
                str(device.rssi) if hasattr(device, "rssi") else "N/A",
            )

        console.print(table)

    asyncio.run(_scan())


@app.command()
def info() -> None:
    """Get information about connected Furby."""

    async def _info() -> None:
        async with FurbyConnect() as furby:
            with console.status("[bold green]Reading device information..."):
                device_info = await furby.get_device_info()

            table = Table(title="Furby Device Information")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="magenta")

            if device_info.manufacturer:
                table.add_row("Manufacturer", device_info.manufacturer)
            if device_info.model_number:
                table.add_row("Model Number", device_info.model_number)
            if device_info.serial_number:
                table.add_row("Serial Number", device_info.serial_number)
            if device_info.hardware_revision:
                table.add_row("Hardware Revision", device_info.hardware_revision)
            if device_info.firmware_revision:
                table.add_row("Firmware Revision", device_info.firmware_revision)
            if device_info.software_revision:
                table.add_row("Software Revision", device_info.software_revision)

            console.print(table)

    asyncio.run(_info())


@app.command()
def antenna(
    red: int = typer.Option(255, help="Red channel (0-255)"),
    green: int = typer.Option(0, help="Green channel (0-255)"),
    blue: int = typer.Option(0, help="Blue channel (0-255)"),
) -> None:
    """Set antenna LED color."""

    async def _antenna() -> None:
        async with FurbyConnect() as furby:
            await furby.set_antenna_color(red, green, blue)
            console.print(f"[green]✓[/green] Antenna set to RGB({red}, {green}, {blue})")

    asyncio.run(_antenna())


@app.command()
def action(
    input: int = typer.Option(..., help="Action input value"),
    index: int = typer.Option(..., help="Action index"),
    subindex: int = typer.Option(..., help="Action subindex"),
    specific: int = typer.Option(..., help="Specific action ID"),
) -> None:
    """Trigger a Furby action sequence."""

    async def _action() -> None:
        async with FurbyConnect() as furby:
            await furby.trigger_action(input, index, subindex, specific)
            console.print(
                f"[green]✓[/green] Action triggered: {input}/{index}/{subindex}/{specific}"
            )

    asyncio.run(_action())


@app.command()
def lcd(enabled: bool = typer.Argument(..., help="True to turn on, False to turn off")) -> None:
    """Control LCD backlight."""

    async def _lcd() -> None:
        async with FurbyConnect() as furby:
            await furby.set_lcd_backlight(enabled)
            console.print(f"[green]✓[/green] LCD backlight {'on' if enabled else 'off'}")

    asyncio.run(_lcd())


@app.command()
def debug() -> None:
    """Cycle through LCD debug menus."""

    async def _debug() -> None:
        async with FurbyConnect() as furby:
            await furby.cycle_debug_menu()
            console.print("[green]✓[/green] Debug menu cycled")

    asyncio.run(_debug())


@app.command()
def name(name_id: int = typer.Argument(..., help="Name ID (0-128)")) -> None:
    """Set Furby name."""
    if not 0 <= name_id <= 128:
        console.print("[red]Error: Name ID must be between 0 and 128[/red]")
        raise typer.Exit(1)

    async def _name() -> None:
        async with FurbyConnect() as furby:
            await furby.set_name(name_id)
            console.print(f"[green]✓[/green] Name set to ID {name_id}")

    asyncio.run(_name())


@app.command()
def monitor(duration: int = typer.Option(0, help="Duration in seconds (0 = infinite)")) -> None:
    """Monitor sensor data in real-time."""

    async def _monitor() -> None:
        async with FurbyConnect() as furby:
            console.print("[bold green]Monitoring sensor data (Ctrl+C to stop)...[/bold green]")

            start_time = asyncio.get_event_loop().time()

            try:
                async for sensor_data in furby.sensor_stream():
                    # Check duration
                    if duration > 0:
                        elapsed = asyncio.get_event_loop().time() - start_time
                        if elapsed > duration:
                            break

                    console.print(
                        Panel(
                            f"[cyan]Timestamp:[/cyan] {sensor_data.timestamp}\n"
                            f"[cyan]Raw Data:[/cyan] {sensor_data.raw_data}",
                            title="Sensor Data",
                        )
                    )

            except KeyboardInterrupt:
                console.print("\n[yellow]Monitoring stopped[/yellow]")

    asyncio.run(_monitor())


@app.command()
def upload_dlc(
    file_path: Path = typer.Argument(..., help="Path to DLC file", exists=True),
    slot: int = typer.Option(2, help="Slot number (default: 2)"),
) -> None:
    """Upload a DLC file to Furby."""

    async def _upload() -> None:
        async with FurbyConnect() as furby:
            dlc_manager = DLCManager(furby)

            with console.status(
                f"[bold green]Uploading {file_path.name} to slot {slot}..."
            ):
                await dlc_manager.upload_dlc(file_path, slot)

            console.print(f"[green]✓[/green] DLC uploaded successfully to slot {slot}")

    asyncio.run(_upload())


@app.command()
def load_dlc(slot: int = typer.Argument(..., help="Slot number")) -> None:
    """Load DLC from slot."""

    async def _load() -> None:
        async with FurbyConnect() as furby:
            dlc_manager = DLCManager(furby)
            await dlc_manager.load_dlc(slot)
            console.print(f"[green]✓[/green] DLC loaded from slot {slot}")

    asyncio.run(_load())


@app.command()
def activate_dlc() -> None:
    """Activate loaded DLC."""

    async def _activate() -> None:
        async with FurbyConnect() as furby:
            dlc_manager = DLCManager(furby)
            await dlc_manager.activate_dlc()
            console.print("[green]✓[/green] DLC activated")

    asyncio.run(_activate())


if __name__ == "__main__":
    app()

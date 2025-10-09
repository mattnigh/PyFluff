# PyFluff Protocol Documentation

This directory contains comprehensive documentation about the Furby Connect Bluetooth Low Energy protocol, file formats, and behavior.

## Documentation Index

### Protocol Documentation
- **[bluetooth.md](bluetooth.md)** - BLE GATT hierarchy and characteristic UUIDs
- **[generalplus.md](generalplus.md)** - GeneralPlus processor commands and responses
- **[nordic.md](nordic.md)** - Nordic processor commands and responses

### Behavior and Content
- **[actions.md](actions.md)** - Overview of action sequences and triggering
- **[actionlist.md](actionlist.md)** - Complete list of all Furby actions with transcriptions
- **[names.md](names.md)** - List of all 129 possible Furby names

### DLC Files and Updates
- **[dlcformat.md](dlcformat.md)** - DLC file format and content structure
- **[flashdlc.md](flashdlc.md)** - How to flash custom DLC files to Furby

## Credits

All protocol documentation in this directory is based on the excellent reverse engineering work done by the bluefluff project:
- **Original Project**: https://github.com/Jeija/bluefluff
- **Author**: Jeija
- **License**: MIT

PyFluff modernizes this work with Python 3.11+, Bleak for BLE communication, and a comprehensive API/CLI interface.

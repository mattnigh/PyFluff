# PyFluff Scripts

This directory contains utility scripts for PyFluff development and maintenance.

## generate_actions_js.py

Generates `web/actions.js` from `docs/actionlist.md`.

**Usage:**
```bash
python scripts/generate_actions_js.py
```

This script parses the markdown action list and creates a JavaScript array with all 1400+ Furby Connect actions, making them searchable in the web interface.

**When to run:**
- After updating `docs/actionlist.md` with new actions
- When the action format changes
- If `web/actions.js` becomes corrupted

**Output:**
- `web/actions.js` - Complete action database with search functionality
- Console output showing statistics about parsed actions

The generated file includes:
- All action definitions with input, index, subindex, specific values
- Category and description for each action
- Cookie management for recent actions
- Search and dropdown UI logic

## test_f2f_connection.py

Diagnostic tool for testing connections to Furbies in F2F (Furby-to-Furby) mode.

**Usage:**
```bash
# Normal diagnostic test
python scripts/test_f2f_connection.py AA:BB:CC:DD:EE:FF

# Aggressive mode with more retries
python scripts/test_f2f_connection.py AA:BB:CC:DD:EE:FF --aggressive
```

**What it tests:**
1. **BLE Scanning**: Verifies Bluetooth is working and can discover devices
2. **Direct Connection**: Tests connection to specific Furby by MAC address
3. **Communication**: Validates commands work (device info, antenna control)

**Modes:**
- **Normal**: 3 retries with 15s timeout per attempt (45s total)
- **Aggressive**: 10 retries with 20s timeout per attempt (200s total)

**When to use:**
- Furby won't connect in F2F mode
- Debugging connection issues
- Verifying MAC address is correct
- Testing after Bluetooth configuration changes
- Troubleshooting range or interference problems

**Output:**
- Colored diagnostic messages
- List of discovered BLE devices
- Connection attempt progress
- Device information if successful
- Detailed troubleshooting tips if failed

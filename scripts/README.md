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

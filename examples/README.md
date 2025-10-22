# PyFluff Examples

This directory contains example scripts demonstrating various PyFluff features.

## Examples

### basic_control.py
Basic Furby control demonstrating connection, antenna colors, and simple actions.

```bash
python examples/basic_control.py
```

### action_sequence.py
**NEW!** Send multiple actions to Furby that execute one after another with configurable delays.

```bash
python examples/action_sequence.py
```

Features:
- Play musical scales (octave notes: Do-Re-Mi-Fa-Sol-La-Ti-Do)
- Create custom action sequences
- Configurable delay between actions (0.1 to 30 seconds)
- Perfect for creating Furby "performances" or scripted behaviors

**Example sequences:**
- Musical notes with 1.5s between each note
- Comedy routine: Giggle → Sing → Puke
- Custom sequences of any documented actions

### mood_monitor.py
Monitor and display Furby's mood state in real-time.

```bash
python examples/mood_monitor.py
```

### custom_dlc.py
Upload custom DLC (DownLoadable Content) files to add new animations, sounds, and behaviors.

```bash
python examples/custom_dlc.py path/to/custom.dlc --slot 2
```

### f2f_connection.py
**NEW!** Connect to Furbies that are in F2F (Furby-to-Furby) communication mode by using their MAC address directly.

```bash
# Show connection method comparison
python examples/f2f_connection.py

# Connect to a specific Furby by MAC address
python examples/f2f_connection.py AA:BB:CC:DD:EE:FF
```

Features:
- Bypass BLE discovery when Furbies are in F2F mode
- Direct connection by MAC address
- Works even when Furby isn't advertising
- Demonstrates connection troubleshooting
- Tests control with antenna color cycling

**Use cases:**
- Connecting to Furbies that are actively communicating with each other
- Reliable connection when normal discovery fails
- Multi-Furby setups where you need to target specific devices
- Development and debugging scenarios

## Requirements

All examples require:
- PyFluff installed and configured
- Furby Connect toy in range
- For HTTP API examples: PyFluff server running (`python -m pyfluff.server`)

## Creating Your Own Examples

You can use these examples as templates for your own Furby projects. Key concepts:

1. **Action Sequences** - Chain multiple actions together
2. **Mood Control** - Adjust Furby's emotional state
3. **Sensor Monitoring** - React to Furby's sensors
4. **DLC Management** - Add custom content

See the main README.md and docs/ directory for complete protocol documentation.

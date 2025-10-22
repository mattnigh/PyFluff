# Connecting to Furbies in F2F (Furby-to-Furby) Mode

## Problem

When Furby Connect toys are actively communicating with each other (F2F mode), they may stop advertising their Bluetooth Low Energy (BLE) presence to conserve power and focus on inter-Furby communication. This makes them invisible to standard BLE discovery scans, resulting in "No Furby devices found" errors.

## Solutions

### 1. Connect by MAC Address (Recommended)

The most reliable way to connect to a Furby in F2F mode is to use its MAC address directly, bypassing discovery entirely.

#### CLI
```bash
# Test connection (with default 3 retries)
python -m pyfluff.cli connect AA:BB:CC:DD:EE:FF

# Use more retries for difficult connections
python -m pyfluff.cli connect AA:BB:CC:DD:EE:FF --retries 5

# Adjust timeout per attempt
python -m pyfluff.cli connect AA:BB:CC:DD:EE:FF --timeout 20 --retries 5

# Control Furby directly
python -m pyfluff.cli antenna --red 255 --green 0 --blue 0 --address AA:BB:CC:DD:EE:FF
```

#### Python API
```python
import asyncio
from pyfluff.furby import FurbyConnect

async def main():
    furby = FurbyConnect()
    # Connect directly by MAC address with retries (helpful for F2F mode)
    await furby.connect(address="AA:BB:CC:DD:EE:FF", timeout=15.0, retries=5)
    
    await furby.set_antenna_color(255, 0, 0)
    await furby.disconnect()

asyncio.run(main())
```

#### Web Interface
1. Navigate to `http://localhost:8080`
2. Enter the Furby's MAC address in the "MAC Address" input field
3. Click "Connect"

#### REST API
```bash
# Connect with default parameters (3 retries, 15s timeout)
curl -X POST http://localhost:8080/connect \
  -H "Content-Type: application/json" \
  -d '{"address": "AA:BB:CC:DD:EE:FF"}'

# Connect with custom retry settings for F2F mode
curl -X POST http://localhost:8080/connect \
  -H "Content-Type: application/json" \
  -d '{"address": "AA:BB:CC:DD:EE:FF", "retries": 5, "timeout": 20.0}'
```

### 2. Find Your Furby's MAC Address

If you don't know your Furby's MAC address, there are several ways to find it:

#### Method A: Scan When Not in F2F Mode
Wake your Furby from F2F mode (by touching sensors or moving it) and scan:

```bash
python -m pyfluff.cli scan
```

Output:
```
Found Furby Devices
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
┃ Name          ┃ Address           ┃ RSSI ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
│ Furby         │ AA:BB:CC:DD:EE:FF │ -45  │
└───────────────┴───────────────────┴──────┘
```

Note down the address for future use.

#### Method B: Scan All BLE Devices
If your Furby isn't appearing in a normal scan, try scanning for all BLE devices:

```bash
python -m pyfluff.cli scan --all
```

This will show **all** BLE devices in range. Look for devices with signal strength (RSSI) around -40 to -60 that might be your Furby.

#### Method C: Check Previous Connections
On Linux/Raspberry Pi, you can check previously paired devices:

```bash
bluetoothctl devices
```

On macOS, open **System Preferences → Bluetooth** to see previously connected devices.

### 3. Wake Furby from F2F Mode

Physical interaction with the Furby can wake it from F2F mode:
- Touch the head sensor
- Stroke the back sensor
- Shake or move the Furby
- Press the tongue sensor

After waking, it should start advertising again and be discoverable via normal scanning.

## Technical Details

### Why This Happens

Bluetooth Low Energy devices can choose when to advertise their presence. During F2F communication, Furbies may:
1. **Stop advertising** to save battery power
2. **Focus processing** on handling F2F communication protocols
3. **Prevent interruption** from new connection attempts

### BLE Connection Process

Normal discovery flow:
```
App → Scan for advertisements → Find Furby → Connect
```

Direct connection flow (bypasses discovery):
```
App → Connect to known MAC address → Success
```

**Enhanced Direct Connection (PyFluff v1.1+):**
```
App → Attempt 1 → Failed
    → Wait 1s
    → Attempt 2 → Failed  
    → Wait 1s
    → Attempt 3 → Success!
```

The direct connection method works because:
- The Furby's BLE radio is still active (just not advertising)
- The operating system's Bluetooth stack can initiate connections without advertisements
- Connection attempts use the MAC address directly at the hardware level
- **Multiple retries** overcome timing issues when Furby is busy with F2F communication

**Default connection parameters:**
- **Timeout**: 15 seconds per attempt (configurable 1-60s)
- **Retries**: 3 attempts (configurable 1-10)
- **Delay**: 1 second between retries
- Total maximum time: timeout × retries (default: 45 seconds)

### F2F Communication Characteristics

The following BLE characteristics are suspected to handle inter-Furby communication:

| UUID | Type | Purpose (Suspected) |
|------|------|---------------------|
| `dab91440b5a1e29cb041bcd562613bde` | Read/Notify | F2F data reception |
| `dab91441b5a1e29cb041bcd562613bde` | Read/Write | F2F data transmission |

**These characteristics are NOT currently implemented in PyFluff.**

Potential F2F capabilities (not confirmed):
- Name exchange between Furbies
- Synchronized actions (singing together, dancing)
- Mood synchronization
- Game coordination (hide and seek, etc.)

### Implementation Notes

PyFluff v1.0+ supports direct MAC address connection:

**FurbyConnect Class:**
```python
async def connect(self, address: str | None = None, timeout: float = 10.0) -> None:
    """
    Connect to a Furby device.
    
    Args:
        address: Optional MAC address to connect to directly (bypasses discovery)
        timeout: Connection timeout in seconds
    """
```

**Server API:**
```python
class ConnectRequest(BaseModel):
    address: str | None = Field(None, description="MAC address to connect to directly")

@app.post("/connect")
async def connect(request: ConnectRequest | None = None) -> CommandResponse:
    """Connect to a Furby device. Optionally provide MAC address to connect directly."""
```

## Troubleshooting

### "Connection failed" Error with MAC Address

**Causes:**
1. Furby is out of range or powered off
2. Furby is in deep sleep mode
3. MAC address is incorrect or formatting issue
4. Bluetooth interference or platform limitations
5. F2F communication is blocking BLE connections

**Solutions:**

**1. Increase Connection Retries**
```bash
# Try with more attempts and longer timeout
python -m pyfluff.cli connect AA:BB:CC:DD:EE:FF --retries 5 --timeout 20
```

**2. Wake the Furby**
- Touch the head sensor repeatedly
- Stroke the back sensor
- Shake or move the Furby
- Press the tongue sensor
- Wait 10-15 seconds after waking before connecting

**3. Verify MAC Address**
```bash
# Scan when Furby is NOT in F2F mode
python -m pyfluff.cli scan

# Or scan all BLE devices
python -m pyfluff.cli scan --all
```

**4. Platform-Specific Fixes**

**macOS:**
- Grant Bluetooth permissions to Terminal/IDE in System Preferences
- Restart Bluetooth: System Preferences → Bluetooth → Turn Off/On
- Forget the device in Bluetooth settings and try again

**Linux/Raspberry Pi:**
```bash
# Restart Bluetooth service
sudo systemctl restart bluetooth

# Check Bluetooth status
sudo systemctl status bluetooth

# Scan with bluetoothctl
bluetoothctl
> scan on
> devices
> connect AA:BB:CC:DD:EE:FF
```

**5. Separate F2F Furbies**
If two Furbies are actively communicating:
- Physically separate them (move them to different rooms)
- Wait 30-60 seconds for F2F session to timeout
- Then attempt connection

**6. Check Signal Strength**
```python
# Use scan to check RSSI (signal strength)
python -m pyfluff.cli scan --all
# Look for RSSI values: -40 to -60 is good, -70+ is weak
```

### "No Furby devices found" Despite Being Visible

**Causes:**
1. Furby name doesn't contain "Furby" string
2. Furby is using custom firmware
3. BLE filtering issue

**Solutions:**
- Use `scan --all` to see all devices
- Connect directly by MAC address if known
- Check Furby's advertised name in Bluetooth settings

### Connection Interrupts F2F Communication

**Expected Behavior:** When you connect to a Furby that's communicating with another Furby, it will likely stop the F2F interaction to handle your connection.

**Workaround:** If you want to observe F2F behavior without interrupting, the F2F characteristics would need to be reverse-engineered and implemented (future work).

## Future Work

To fully support F2F observation and control, the following would be needed:

1. **Reverse engineer F2F protocol:**
   - Capture F2F communication packets
   - Analyze characteristic `dab91440`/`dab91441` data
   - Document message formats and sequences

2. **Implement F2F snooping:**
   - Connect to Furby without interrupting F2F
   - Subscribe to F2F characteristics
   - Log and decode F2F messages

3. **Implement F2F control:**
   - Simulate another Furby
   - Send coordinated commands
   - Enable multi-Furby choreography

## References

- [Bluetooth Low Energy Specification](https://www.bluetooth.com/specifications/specs/core-specification-5-3/)
- [Bluefluff Original Project](https://github.com/Jeija/bluefluff) - Original reverse engineering work
- [PyFluff Bluetooth Documentation](bluetooth.md) - Complete BLE characteristic reference
- [Bleak BLE Library](https://github.com/hbldh/bleak) - Python BLE library used by PyFluff

---

> **Note:** This documentation is based on observed behavior and hypothesis. The F2F protocol has not been fully reverse-engineered. Contributions and findings are welcome!

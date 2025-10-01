# Debugging Web UI Command Issues

## Changes Made

I've made several fixes to resolve the web UI command sending issues:

### 1. Static Files Not Being Served
**Problem**: The server imported `StaticFiles` but never mounted the `/web` directory.

**Fix**: Added static file mounting in `server.py`:
```python
web_dir = Path(__file__).parent.parent / "web"
if web_dir.exists():
    app.mount("/static", StaticFiles(directory=str(web_dir)), name="static")
```

Updated paths in `index.html`:
- Changed `href="style.css"` to `href="/static/style.css"`
- Changed `src="app.js"` to `src="/static/app.js"`

### 2. Missing CORS Middleware
**Problem**: Browser might block API requests due to CORS policy.

**Fix**: Added CORS middleware in `server.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Auto-Connect on Startup
**Problem**: Server was trying to auto-connect to Furby on startup, which could fail and leave the connection in a bad state.

**Fix**: Changed startup behavior to NOT auto-connect. Users must now click "Connect" in the web UI.

### 4. Better Error Handling
**Problem**: Errors weren't being logged properly, making debugging difficult.

**Fix**: Added detailed logging and error handling to all command endpoints:
```python
logger.info(f"Setting antenna color: RGB({color.red}, {color.green}, {color.blue})")
try:
    await fb.set_antenna_color(color.red, color.green, color.blue)
    logger.info("Antenna color set successfully")
except Exception as e:
    logger.error(f"Failed to set antenna color: {e}")
    raise HTTPException(status_code=500, detail=str(e))
```

## Testing Steps

### Step 1: Test Direct Connection
Run the test script to verify BLE communication works:

```bash
cd /Users/martin/src/PyFluff
source venv/bin/activate
python test_connection.py
```

If this works, the BLE communication is fine and the issue is with the web server.

If this fails, check:
- Is Furby powered on?
- Is Bluetooth enabled on your Mac?
- Does your Mac have permission to use Bluetooth?
- Is Furby in range?

### Step 2: Start the Server
```bash
python -m pyfluff.server
```

Watch the logs for any errors on startup.

### Step 3: Test the Web UI
1. Open http://localhost:8080 in your browser
2. Open browser Developer Tools (F12 or Cmd+Option+I)
3. Go to the Console tab
4. Click "Connect" button
5. Watch for any JavaScript errors in the console
6. Watch for any errors in the server terminal

### Step 4: Check Network Requests
In browser Developer Tools:
1. Go to Network tab
2. Click "Connect" button
3. Look for the POST request to `/connect`
4. Check the response - is it 200 OK or an error?

### Step 5: Try Commands
Once connected:
1. Try setting antenna color
2. Watch both browser console and server logs
3. Look for any errors in either place

## Common Issues

### Issue: "Failed to fetch" errors in browser
**Cause**: Static files not loading, CORS issues, or server not running

**Solutions**:
- Make sure server is running
- Check that http://localhost:8080/static/app.js loads (should show JavaScript code)
- Check browser console for CORS errors

### Issue: Commands seem to work but Furby doesn't respond
**Cause**: BLE connection issue or command format problem

**Solutions**:
- Run `test_connection.py` to verify direct BLE communication
- Check server logs for BLE errors
- Make sure only ONE application is trying to connect to Furby at a time
- Try power cycling the Furby

### Issue: "Not connected to Furby" error
**Cause**: Connection lost or never established

**Solutions**:
- Click "Connect" button in UI
- Check server logs for connection errors
- Verify Furby is in range and powered on
- Try the test script to diagnose BLE issues

### Issue: Connection works but specific commands fail
**Cause**: Command packet format issue

**Solutions**:
- Check server logs for the exact error
- Compare with working bluefluff-modern implementation
- Verify command bytes in `protocol.py`

## Comparing with bluefluff-modern

If you have the working Node.js implementation, you can compare:

1. **Protocol packets**: Use Wireshark or `btmon` to capture actual BLE packets from both implementations
2. **Command format**: Check that the byte arrays match between Node and Python versions
3. **Timing**: Some commands might need delays between them

## Server Log Analysis

Look for these patterns in the server logs:

**Good connection**:
```
INFO - PyFluff server starting up...
INFO - Scanning for Furby devices (timeout: 10.0s)...
INFO - Found 1 Furby device(s)
INFO - Connecting to Furby at XX:XX:XX:XX:XX:XX...
INFO - Connected successfully
INFO - Subscribed to GeneralPlus notifications
INFO - Subscribed to Nordic notifications
INFO - Started idle keepalive
```

**Command execution**:
```
INFO - Setting antenna color: RGB(255, 0, 0)
DEBUG - GP write: 14ff0000
INFO - Antenna color set successfully
```

**Error pattern**:
```
ERROR - Failed to set antenna color: Not connected to Furby
```

## Next Steps

If the above fixes don't resolve the issue, check:

1. Verify the command packet format matches the original bluefluff implementation
2. Check if there's a timing issue (commands sent too fast?)
3. Verify the Furby is actually in "app mode" and ready to receive commands
4. Check if there's a firmware version issue with your specific Furby

## MacOS-Specific Issues

MacOS BLE can be finicky. Try these:

1. **Reset Bluetooth**:
   ```bash
   sudo pkill bluetoothd
   ```

2. **Check permissions**: Make sure Terminal (or your IDE) has Bluetooth permission in System Preferences → Privacy & Security → Bluetooth

3. **Try from different app**: If it works from Terminal but not VS Code, check VS Code's Bluetooth permissions

4. **Check Bluetooth status**:
   ```bash
   system_profiler SPBluetoothDataType
   ```

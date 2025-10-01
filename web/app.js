// PyFluff Web Interface JavaScript

const API_BASE = window.location.origin;
let ws = null;
let isMonitoring = false;

// Utility functions
function log(message, type = 'info') {
    const logDiv = document.getElementById('log');
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    logDiv.insertBefore(entry, logDiv.firstChild);
    
    // Keep only last 50 entries
    while (logDiv.children.length > 50) {
        logDiv.removeChild(logDiv.lastChild);
    }
}

async function apiCall(endpoint, method = 'GET', body = null) {
    try {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        
        if (body) {
            options.body = JSON.stringify(body);
        }
        
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Request failed');
        }
        
        return data;
    } catch (error) {
        log(`Error: ${error.message}`, 'error');
        throw error;
    }
}

// Update status
async function updateStatus() {
    try {
        const status = await apiCall('/status');
        const statusDiv = document.getElementById('status');
        const deviceInfo = document.getElementById('device-info');
        
        if (status.connected) {
            statusDiv.textContent = 'Connected';
            statusDiv.className = 'status connected';
            
            let info = `Device: ${status.device_name || 'Unknown'}<br>`;
            info += `Address: ${status.device_address || 'Unknown'}<br>`;
            if (status.firmware_version) {
                info += `Firmware: ${status.firmware_version}`;
            }
            deviceInfo.innerHTML = info;
        } else {
            statusDiv.textContent = 'Disconnected';
            statusDiv.className = 'status disconnected';
            deviceInfo.innerHTML = '';
        }
    } catch (error) {
        console.error('Failed to update status:', error);
    }
}

// Connection handlers
document.getElementById('btn-connect').addEventListener('click', async () => {
    try {
        const result = await apiCall('/connect', 'POST');
        log(result.message, 'success');
        await updateStatus();
    } catch (error) {
        log(`Connection failed: ${error.message}`, 'error');
    }
});

document.getElementById('btn-disconnect').addEventListener('click', async () => {
    try {
        const result = await apiCall('/disconnect', 'POST');
        log(result.message, 'success');
        await updateStatus();
    } catch (error) {
        log(`Disconnect failed: ${error.message}`, 'error');
    }
});

// Antenna color control
const redSlider = document.getElementById('red-slider');
const greenSlider = document.getElementById('green-slider');
const blueSlider = document.getElementById('blue-slider');
const colorPreview = document.getElementById('color-preview');

function updateColorPreview() {
    const r = redSlider.value;
    const g = greenSlider.value;
    const b = blueSlider.value;
    
    document.getElementById('red-value').textContent = r;
    document.getElementById('green-value').textContent = g;
    document.getElementById('blue-value').textContent = b;
    
    colorPreview.style.background = `rgb(${r}, ${g}, ${b})`;
}

redSlider.addEventListener('input', updateColorPreview);
greenSlider.addEventListener('input', updateColorPreview);
blueSlider.addEventListener('input', updateColorPreview);

document.getElementById('btn-set-antenna').addEventListener('click', async () => {
    try {
        const result = await apiCall('/antenna', 'POST', {
            red: parseInt(redSlider.value),
            green: parseInt(greenSlider.value),
            blue: parseInt(blueSlider.value)
        });
        log(result.message, 'success');
    } catch (error) {
        log(`Failed to set antenna: ${error.message}`, 'error');
    }
});

// Color presets
document.querySelectorAll('.color-preset').forEach(btn => {
    btn.addEventListener('click', () => {
        const [r, g, b] = btn.dataset.color.split(',').map(Number);
        redSlider.value = r;
        greenSlider.value = g;
        blueSlider.value = b;
        updateColorPreview();
    });
});

// Quick actions
document.querySelectorAll('.btn-action[data-action]').forEach(btn => {
    btn.addEventListener('click', async () => {
        const [input, index, subindex, specific] = btn.dataset.action.split(',').map(Number);
        try {
            const result = await apiCall('/action', 'POST', { input, index, subindex, specific });
            log(`Action triggered: ${btn.textContent}`, 'success');
        } catch (error) {
            log(`Action failed: ${error.message}`, 'error');
        }
    });
});

// LCD control
document.getElementById('btn-lcd-on').addEventListener('click', async () => {
    try {
        await apiCall('/lcd/true', 'POST');
        log('LCD turned on', 'success');
    } catch (error) {
        log(`LCD control failed: ${error.message}`, 'error');
    }
});

document.getElementById('btn-lcd-off').addEventListener('click', async () => {
    try {
        await apiCall('/lcd/false', 'POST');
        log('LCD turned off', 'success');
    } catch (error) {
        log(`LCD control failed: ${error.message}`, 'error');
    }
});

// Debug menu
document.getElementById('btn-debug').addEventListener('click', async () => {
    try {
        await apiCall('/debug', 'POST');
        log('Debug menu cycled', 'success');
    } catch (error) {
        log(`Debug failed: ${error.message}`, 'error');
    }
});

// Custom action
document.getElementById('btn-custom-action').addEventListener('click', async () => {
    try {
        const result = await apiCall('/action', 'POST', {
            input: parseInt(document.getElementById('action-input').value),
            index: parseInt(document.getElementById('action-index').value),
            subindex: parseInt(document.getElementById('action-subindex').value),
            specific: parseInt(document.getElementById('action-specific').value)
        });
        log('Custom action triggered', 'success');
    } catch (error) {
        log(`Custom action failed: ${error.message}`, 'error');
    }
});

// Mood control
document.getElementById('btn-set-mood').addEventListener('click', async () => {
    try {
        const result = await apiCall('/mood', 'POST', {
            type: document.getElementById('mood-type').value,
            action: document.getElementById('mood-action').value,
            value: parseInt(document.getElementById('mood-value').value)
        });
        log(result.message, 'success');
    } catch (error) {
        log(`Mood update failed: ${error.message}`, 'error');
    }
});

// DLC management
document.getElementById('btn-upload-dlc').addEventListener('click', async () => {
    const fileInput = document.getElementById('dlc-file');
    const slot = parseInt(document.getElementById('dlc-slot').value);
    
    if (!fileInput.files.length) {
        log('Please select a DLC file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    try {
        const response = await fetch(`${API_BASE}/dlc/upload?slot=${slot}`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            log(result.message, 'success');
        } else {
            throw new Error(result.detail || 'Upload failed');
        }
    } catch (error) {
        log(`DLC upload failed: ${error.message}`, 'error');
    }
});

document.getElementById('btn-load-dlc').addEventListener('click', async () => {
    const slot = parseInt(document.getElementById('dlc-slot').value);
    try {
        const result = await apiCall(`/dlc/load/${slot}`, 'POST');
        log(result.message, 'success');
    } catch (error) {
        log(`DLC load failed: ${error.message}`, 'error');
    }
});

document.getElementById('btn-activate-dlc').addEventListener('click', async () => {
    try {
        const result = await apiCall('/dlc/activate', 'POST');
        log(result.message, 'success');
    } catch (error) {
        log(`DLC activation failed: ${error.message}`, 'error');
    }
});

// Sensor monitoring
document.getElementById('btn-monitor').addEventListener('click', () => {
    if (isMonitoring) {
        stopMonitoring();
    } else {
        startMonitoring();
    }
});

function startMonitoring() {
    const btn = document.getElementById('btn-monitor');
    const sensorDiv = document.getElementById('sensor-data');
    
    btn.textContent = 'Stop Monitoring';
    btn.className = 'btn btn-secondary';
    isMonitoring = true;
    
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(`${wsProtocol}//${window.location.host}/ws/sensors`);
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const entry = document.createElement('div');
        entry.textContent = `[${new Date(data.timestamp * 1000).toLocaleTimeString()}] ${data.raw_data}`;
        sensorDiv.insertBefore(entry, sensorDiv.firstChild);
        
        // Keep only last 20 entries
        while (sensorDiv.children.length > 20) {
            sensorDiv.removeChild(sensorDiv.lastChild);
        }
    };
    
    ws.onerror = (error) => {
        log('WebSocket error', 'error');
        stopMonitoring();
    };
    
    ws.onclose = () => {
        if (isMonitoring) {
            log('Monitoring connection closed', 'error');
            stopMonitoring();
        }
    };
    
    log('Started sensor monitoring', 'success');
}

function stopMonitoring() {
    const btn = document.getElementById('btn-monitor');
    btn.textContent = 'Start Monitoring';
    btn.className = 'btn btn-primary';
    isMonitoring = false;
    
    if (ws) {
        ws.close();
        ws = null;
    }
    
    log('Stopped sensor monitoring', 'success');
}

// Initialize
updateStatus();
setInterval(updateStatus, 5000); // Update status every 5 seconds

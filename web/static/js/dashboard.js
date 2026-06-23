const WS_URL = `ws://${window.location.host}/ws`;
const API_BASE = '/api/v1';

let ws = null;
let reconnectTimer = null;

function connectWebSocket() {
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
        document.getElementById('connection-status').className = 'status-dot connected';
        addLog('WebSocket connected', 'info');
        clearTimeout(reconnectTimer);
    };

    ws.onclose = () => {
        document.getElementById('connection-status').className = 'status-dot disconnected';
        addLog('WebSocket disconnected, reconnecting...', 'warning');
        reconnectTimer = setTimeout(connectWebSocket, 3000);
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWSMessage(data);
    };

    ws.onerror = () => {
        addLog('WebSocket error', 'error');
    };
}

function handleWSMessage(data) {
    switch(data.type) {
        case 'connection':
            addLog(`[WS] ${data.message} (${data.clients} clients)`, 'info');
            break;
        case 'pong':
            break;
        default:
            addLog(`[WS] ${JSON.stringify(data)}`, 'info');
    }
}

function addLog(message, type = 'info') {
    const container = document.getElementById('log-container');
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    container.appendChild(entry);
    container.scrollTop = container.scrollHeight;
}

async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        return await response.json();
    } catch (error) {
        addLog(`API Error: ${error.message}`, 'error');
        return null;
    }
}

async function updateStatus() {
    const data = await fetchAPI('/status');
    if (!data) return;

    document.getElementById('engine-status').textContent = data.engine_running ? 'Online' : 'Offline';
    document.getElementById('uptime').textContent = `Uptime: ${data.uptime}s`;
    document.getElementById('rotations').textContent = data.identities_rotated;
    document.getElementById('proxy-count').textContent = data.active_proxies;
    document.getElementById('requests').textContent = data.requests_sent;
    document.getElementById('obfuscation').textContent = `Obfuscation: ${data.current_method}`;
    document.getElementById('chain-info').textContent = `Spoofing: ${data.spoofing_active ? 'ON' : 'OFF'}`;
}

async function rotateIdentity() {
    const btn = document.getElementById('rotate-btn');
    btn.disabled = true;
    btn.textContent = 'Rotating...';

    const data = await fetchAPI('/rotate', { method: 'POST' });
    if (data && data.success) {
        addLog(`Identity rotated successfully! (Total: ${data.total_rotations})`, 'info');
        updateStatus();
    } else {
        addLog('Identity rotation failed', 'error');
    }

    btn.disabled = false;
    btn.textContent = 'Rotate Now';
}

async function refreshChain() {
    const data = await fetchAPI('/chain');
    if (!data) return;

    const container = document.getElementById('chain-visual');
    container.innerHTML = '<span class="chain-node">You</span>';

    data.chain.forEach((node, index) => {
        container.innerHTML += '<span class="chain-arrow">→</span>';
        container.innerHTML += `<span class="chain-node">${node}</span>`;
    });

    if (data.chain.length === 0) {
        container.innerHTML += '<span class="chain-arrow">→</span>';
        container.innerHTML += '<span class="chain-node">Direct</span>';
    }

    container.innerHTML += '<span class="chain-arrow">→</span>';
    container.innerHTML += '<span class="chain-node">Target</span>';
}

async function runScan() {
    const target = document.getElementById('scan-target').value;
    const portsStr = document.getElementById('scan-ports').value;

    if (!target) {
        addLog('Please enter a target IP', 'warning');
        return;
    }

    const ports = portsStr ? portsStr.split(',').map(p => parseInt(p.trim())) : [22, 80, 443];

    const btn = document.getElementById('scan-btn');
    btn.disabled = true;
    btn.textContent = 'Scanning...';

    addLog(`Starting stealth scan on ${target}:${ports.join(',')}`, 'info');

    const data = await fetchAPI('/scan', {
        method: 'POST',
        body: JSON.stringify({ target, ports })
    });

    const container = document.getElementById('scan-results');
    container.innerHTML = '';

    if (data && data.open_ports) {
        data.open_ports.forEach(port => {
            container.innerHTML += `<div class="scan-result-item open">Port ${port}: OPEN</div>`;
        });
        data.filtered_ports.forEach(port => {
            container.innerHTML += `<div class="scan-result-item filtered">Port ${port}: FILTERED</div>`;
        });
        addLog(`Scan complete: ${data.open_ports.length} open, ${data.filtered_ports.length} filtered`, 'info');
    }

    btn.disabled = false;
    btn.textContent = 'Stealth Scan';
}

async function testConnection() {
    const btn = document.getElementById('test-btn');
    btn.disabled = true;
    btn.textContent = 'Testing...';

    addLog('Testing ghost connection...', 'info');

    const data = await fetchAPI('/test', { method: 'POST' });

    const container = document.getElementById('test-result');
    if (data && data.status) {
        container.innerHTML = `
            <div style="color: #9ece6a;">Status: ${data.status}</div>
            <pre style="color: #7aa2f7; margin-top: 10px;">${JSON.stringify(data, null, 2)}</pre>
        `;
        addLog('Connection test successful', 'info');
    } else {
        container.innerHTML = '<div style="color: #f7768e;">Connection test failed</div>';
        addLog('Connection test failed', 'error');
    }

    btn.disabled = false;
    btn.textContent = 'Test Ghost Connection';
}

document.getElementById('rotate-btn').addEventListener('click', rotateIdentity);
document.getElementById('refresh-chain-btn').addEventListener('click', refreshChain);
document.getElementById('scan-btn').addEventListener('click', runScan);
document.getElementById('test-btn').addEventListener('click', testConnection);

connectWebSocket();
updateStatus();
refreshChain();

setInterval(updateStatus, 5000);
setInterval(refreshChain, 10000);
import subprocess
import platform
import re
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

# --- API CONFIGURATION ---
app = FastAPI(
    title="GameRoute Performance API",
    description="Advanced network latency tracking system for gaming infrastructure.",
    version="1.0.0"
)

# Pre-defined game server infrastructure
SERVER_INFRA = {
    "tr": {"name": "Turkey (Istanbul)", "ip": "104.160.141.3"},
    "eu": {"name": "Europe (Frankfurt)", "ip": "104.160.142.3"},
    "na": {"name": "North America (Chicago)", "ip": "104.160.131.3"},
    "test": {"name": "Google DNS (Global)", "ip": "8.8.8.8"}
}

# --- CORE ENGINE ---

def execute_latency_check(target_host: str):
    """
    Executes a system-level ICMP ping and parses the result using Regex.
    Supports cross-platform compatibility (Windows & Linux).
    """
    # Determine OS-specific ping parameters
    os_type = platform.system().lower()
    flag = '-n' if os_type == 'windows' else '-c'
    
    execution_cmd = ['ping', flag, '1', target_host]
    
    try:
        # Run terminal command and capture output
        process = subprocess.run(execution_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        
        if process.returncode == 0:
            terminal_output = process.stdout.lower()
            
            # Professional Regex Pattern: Captures digits immediately followed by 'ms'
            latency_pattern = re.search(r'(\d+)\s*ms', terminal_output)
            
            if latency_pattern:
                ms_value = int(latency_pattern.group(1))
                return {"status": "Online", "latency_ms": ms_value}
            
            return {"status": "Online", "latency_ms": "Parse Error"}
            
        return {"status": "Offline", "latency_ms": 0}

    except subprocess.TimeoutExpired:
        return {"status": "Timeout", "latency_ms": 0}
    except Exception as error:
        return {"status": "Error", "latency_ms": 0, "detail": str(error)}

# --- API ENDPOINTS ---

@app.get("/api/v1/status/{region}")
async def get_region_status(region: str):
    """Retrieves status for pre-defined server regions."""
    region_key = region.lower()
    
    if region_key not in SERVER_INFRA:
        raise HTTPException(status_code=404, detail="Region not supported in infrastructure.")
    
    target = SERVER_INFRA[region_key]
    network_result = execute_latency_check(target["ip"])
    
    return {
        "region_name": target["name"],
        "region_code": region_key.upper(),
        "network_data": network_result
    }

@app.get("/api/v1/analyze")
async def analyze_custom_ip(target_ip: str = Query(..., description="The IP address to analyze")):
    """Performs a real-time latency analysis on any provided IP address."""
    network_result = execute_latency_check(target_ip)
    
    return {
        "target": target_ip,
        "results": network_result
    }

# --- FRONTEND DASHBOARD ---

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Serves the professional monitoring dashboard."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>GameRoute | Infrastructure Monitor</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            :root { --bg: #0f172a; --card: #1e293b; --accent: #38bdf8; --text: #f8fafc; --success: #4ade80; }
            body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
            .dashboard { background: var(--card); border-radius: 1.5rem; padding: 2.5rem; width: 100%; max-width: 480px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }
            h1 { font-weight: 700; color: var(--accent); margin-bottom: 0.5rem; }
            .subtitle { color: #94a3b8; margin-bottom: 2rem; font-size: 0.9rem; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; margin-bottom: 2rem; }
            button { background: #334155; color: white; border: 1px solid #475569; padding: 0.8rem; border-radius: 0.75rem; font-weight: 600; cursor: pointer; transition: all 0.2s; }
            button:hover { background: var(--accent); color: var(--bg); border-color: var(--accent); transform: translateY(-2px); }
            .input-box { border-top: 1px solid #334155; padding-top: 1.5rem; }
            input { width: 100%; background: var(--bg); border: 1px solid #334155; border-radius: 0.75rem; padding: 0.8rem; color: white; margin-bottom: 0.8rem; box-sizing: border-box; }
            .main-btn { width: 100%; background: var(--accent) !important; color: var(--bg) !important; }
            #status-display { margin-top: 2rem; background: var(--bg); padding: 1.2rem; border-radius: 1rem; border: 1px solid #334155; min-height: 24px; font-weight: 600; }
            .status-ok { color: var(--success); }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <h1>GameRoute Pro</h1>
            <p class="subtitle">Global Infrastructure Latency Monitor</p>
            
            <div class="grid">
                <button onclick="runCheck('tr')">Turkey</button>
                <button onclick="runCheck('eu')">Europe</button>
                <button onclick="runCheck('na')">North America</button>
                <button onclick="runCheck('test')">Diagnostics</button>
            </div>

            <div class="input-box">
                <input type="text" id="targetIp" placeholder="Enter custom IP (e.g. 1.1.1.1)">
                <button class="main-btn" onclick="runCustom()">Analyze Custom Node</button>
            </div>

            <div id="status-display">System ready for analysis...</div>
        </div>

        <script>
            async function runCheck(region) {
                const display = document.getElementById('status-display');
                display.innerHTML = `<span style="color: #94a3b8">Connecting to ${region.toUpperCase()}...</span>`;
                const res = await fetch(`/api/v1/status/${region}`);
                const data = await res.json();
                render(data.network_data, data.region_name);
            }

            async function runCustom() {
                const ip = document.getElementById('targetIp').value;
                if(!ip) return;
                const display = document.getElementById('status-display');
                display.innerHTML = `<span style="color: #94a3b8">Analyzing ${ip}...</span>`;
                const res = await fetch(`/api/v1/analyze?target_ip=${ip}`);
                const data = await res.json();
                render(data.results, data.target);
            }

            function render(res, title) {
                const display = document.getElementById('status-display');
                const color = res.status === "Online" ? "#4ade80" : "#f87171";
                display.innerHTML = `<span style="color: ${color}">● ${res.status}</span> | ${title} | <span style="color: var(--accent)">${res.latency_ms} ms</span>`;
            }
        </script>
    </body>
    </html>
    """
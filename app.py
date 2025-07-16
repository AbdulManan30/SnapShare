from flask import Flask, request, render_template_string
import subprocess
import platform

app = Flask(__name__)
shared_text = ""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SnapShare – Devices</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #f4f4f8; padding: 30px; max-width: 800px; margin: auto; color: #333; }
        h1, h2 { text-align: center; color: #2b2d42; }
        form { display: flex; gap: 10px; justify-content: center; margin-bottom: 30px; }
        input[name="text"] { flex: 1; padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 6px; }
        button { padding: 10px 15px; background: #2b2d42; color: white; border: none; border-radius: 6px; cursor: pointer; }
        button:hover { background: #1f2233; }
        .text-box { background: white; border: 1px solid #ddd; padding: 15px; border-radius: 8px; margin-bottom: 40px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
        th, td { padding: 10px 14px; border-bottom: 1px solid #eee; text-align: left; }
        th { background: #343a40; color: white; }
        tr:hover { background: #f1f1f1; }
        footer { margin-top: 30px; text-align: center; color: #888; font-size: 14px; }
    </style>
</head>
<body>
    <h1>SnapShare</h1>
    <h2>Shared Text on Local Network</h2>
    <form method="post">
        <input name="text" value="{{ text }}" placeholder="Type shared message here..." />
        <button type="submit">Save</button>
    </form>
  <div class="text-box">
    <strong>Current Shared Text:</strong>
    <p id="shared-text">
        {% if text == "" %}
            There is no message yet.
        {% else %}
           <b>Writed Text:</b> {{ text }}
        {% endif %}
    </p>
</div>

    <h2>Connected Devices</h2>
    <table>
        <thead>
            <tr>
                <th>IP Address</th>
                <th>Device Name (Hostname)</th>
            </tr>
        </thead>
        <tbody id="device-table">
            {% for device in devices %}
            <tr>
                <td>{{ device.ip }}</td>
                <td>{{ device.hostname }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <footer>Devices detected on your local WiFi using Nmap</footer>
</body>
</html>
"""

def scan_devices():
    try:
        cmd = ["nmap", "-sn", "192.168.18.0/24"]
        if platform.system() != "Windows":
            cmd.insert(0, "sudo")

        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        devices = []
        current_ip = None
        hostname = "Unknown"

        for line in output.splitlines():
            if line.startswith("Nmap scan report for"):
                parts = line.split()
                if len(parts) == 5:
                    hostname = parts[4]
                    current_ip = parts[4]
                elif len(parts) == 6:
                    hostname = parts[4]
                    current_ip = parts[5].strip("()")
            if "Host is up" in line and current_ip:
                devices.append({"ip": current_ip, "hostname": hostname})

        return devices
    except Exception as e:
        return [{"ip": "Error", "hostname": str(e)}]

@app.route("/", methods=["GET", "POST"])
def index():
    global shared_text
    if request.method == "POST":
        shared_text = request.form["text"]
        devices = scan_devices()
        return render_template_string(HTML_TEMPLATE, text=shared_text, devices=devices)
    
    devices = scan_devices()
    return render_template_string(HTML_TEMPLATE, text=shared_text, devices=devices)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

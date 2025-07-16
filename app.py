from flask import Flask, request, render_template, send_file, redirect, url_for
import subprocess, platform, os, io
from file_feature import handle_file_upload, get_latest_uploaded_file, delete_all_files

app = Flask(__name__)
shared_text = ""

def scan_devices():
    if os.environ.get("DISABLE_SCAN") == "true":
        return [{"ip": "N/A", "hostname": "Device scanning disabled"}]
    try:
        cmd = ["nmap", "-sn", "192.168.18.0/24"]
        if platform.system() != "Windows":
            cmd.insert(0, "sudo")

        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout

        devices = []
        current_ip, hostname = None, "Unknown"

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
    filename = ""

    if request.method == "POST":
        shared_text = request.form.get("text", "")
        filename = handle_file_upload(request)

    filename = get_latest_uploaded_file()
    if not os.path.exists(os.path.join("uploads", filename)):
        filename = ""

    devices = scan_devices()
    return render_template("index.html", text=shared_text, devices=devices, filename=filename)

@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join("uploads", filename)
    if not os.path.isfile(file_path):
        return redirect(url_for("index"))

    with open(file_path, "rb") as f:
        file_data = f.read()

    delete_all_files()

    return send_file(
        io.BytesIO(file_data),
        as_attachment=True,
        download_name=filename,
        mimetype="application/octet-stream"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

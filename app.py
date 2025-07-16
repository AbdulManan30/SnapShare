from flask import Flask, request, render_template_string, send_file, redirect, url_for
import subprocess
import platform
from file_feature import handle_file_upload, get_latest_uploaded_file
from htmlCode import HTML_TEMPLATE
import os
import io

app = Flask(__name__)
shared_text = ""

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
        shared_text = request.form.get("text", "")
        filename = handle_file_upload()
        devices = scan_devices()
        return render_template_string(HTML_TEMPLATE(), text=shared_text, devices=devices, filename=filename)

    # Check latest file
    filename = get_latest_uploaded_file()
    file_path = os.path.join("uploads", filename)

    # Clear filename if file doesn't exist (was deleted)
    if not os.path.exists(file_path):
        filename = ""

    devices = scan_devices()
    return render_template_string(HTML_TEMPLATE(), text=shared_text, devices=devices, filename=filename)


@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join("uploads", filename)

    if not os.path.isfile(file_path):
        return redirect(url_for("index"))

    # Read file into memory
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Delete all files in uploads folder
    for f in os.listdir("uploads"):
        try:
            os.remove(os.path.join("uploads", f))
        except:
            pass

    # Send file from memory
    return send_file(
        io.BytesIO(file_data),
        as_attachment=True,
        download_name=filename,
        mimetype="application/octet-stream"
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

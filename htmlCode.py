def HTML_TEMPLATE():
    return  '''
<!DOCTYPE html>
<html>
<head>
    <title>SnapShare – Devices</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        /* Global Styles */
        * {
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #eef2f3, #dfe6e9);
            padding: 30px;
            max-width: 900px;
            margin: auto;
            color: #333;
            animation: fadeIn 0.6s ease-in-out;
        }

        h1, h2 {
            text-align: center;
            color: #2d3436;
            margin-bottom: 10px;
        }

        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-bottom: 30px;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.1);
            animation: fadeInUp 0.5s ease forwards;
        }

        input[type="file"] {
            padding: 12px 16px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        input[type="file"]:focus {
            border-color: #6c5ce7;
            outline: none;
            box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.1);
        }
        .input-group {
        position: relative;
        margin-top: 10px;
        width: 100%;
      }

    .input-group input {
        width: 100%;
        padding: 16px 16px 16px 20px;
        font-size: 16px;
        border: 2px solid #dcdde1;
        border-radius: 10px;
        outline: none;
        transition: border 0.3s, box-shadow 0.3s;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .input-group input:focus {
        border-color: #6c5ce7;
        box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.1);
    }

    .input-group label {
        position: absolute;
        top: 50%;
        left: 20px;
        transform: translateY(-50%);
        background: white;
        padding: 0 6px;
        color: #888;
        font-size: 16px;
        pointer-events: none;
        transition: all 0.2s ease;
    }

    .input-group input:focus + label,
    .input-group input:not(:placeholder-shown):not(:focus) + label,
    .input-group input:not(:empty):not(:focus) + label {
        top: 6px;
        left: 16px;
        font-size: 13px;
        color: #6c5ce7;
    }

        button {
            padding: 12px;
            font-size: 16px;
            background: #6c5ce7;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        button:hover {
            background: #5a4edc;
            transform: scale(1.03);
        }

        .text-box, .file-box {
            background: white;
            border: 1px solid #ddd;
            padding: 18px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            animation: fadeInUp 0.6s ease;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            animation: fadeInUp 0.6s ease;
        }

        th, td {
            padding: 12px 14px;
            border-bottom: 1px solid #eee;
            text-align: left;
        }

        th {
            background: #6c5ce7;
            color: white;
        }

        tr:hover {
            background: #f1f1f1;
        }

        footer {
            margin-top: 40px;
            text-align: center;
            color: #888;
            font-size: 14px;
            animation: fadeIn 1s ease-in;
        }

        @keyframes fadeIn {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }

        @keyframes fadeInUp {
            0% {
                opacity: 0;
                transform: translateY(20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        a {
            text-decoration: none;
            color: #0984e3;
            font-weight: bold;
        }

        a:hover {
            text-decoration: underline;
        }

        .file-box button {
            margin-top: 10px;
            background: #00b894;
        }

        .file-box button:hover {
            background: #019874;
        }
    </style>
</head>
<body>
    <h1>📡 SnapShare</h1>
    <h2>Share Text & Files on Local Network</h2>

    <form method="post" enctype="multipart/form-data">
        <div class="input-group">
            <input type="text" name="text" id="text-input" required value="{{ text }}">
            <label for="text-input">💬 Enter shared message...</label>
        </div>

        {% if not filename %}
            <input type="file" name="file" />
        {% endif %}

        <button type="submit">Submit</button>
    </form>

    <div class="text-box">
        <strong>Current Shared Text:</strong>
        <p id="shared-text">
            {% if text == "" %}
                <i>There is no message yet.</i>
            {% else %}
                <b>Writed Text:</b> {{ text }}
            {% endif %}
        </p>
    </div>

    {% if filename %}
    <div class="file-box">
        <strong>Shared File:</strong>
        <form action="/download/{{ filename }}" method="get">
            <p>{{ filename }}</p>
            <button type="submit">📥 Download File</button>
        </form>
    </div>

    {% endif %}


    <h2>Connected Devices</h2>
    <table>
        <thead>
            <tr>
                <th>IP Address</th>
                <th>Device Name</th>
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

    <footer>🌐 Devices detected on your local WiFi using Nmap</footer>
</body>
</html>

'''
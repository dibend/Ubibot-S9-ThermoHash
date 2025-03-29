# Ubibot-S9-ThermoHash
Ubibot Temp Sensor S9 Heat Regulation<br>
<img src="https://github.com/dibend/Ubibot-S9-ThermoHash/blob/main/thermostat.png?raw=true" width="500" alt="thermostat">
<br>
<h1>⚡ ThermoHash Dashboard — S9/S9i Smart Power Control</h1>

<p>
A FastAPI-based control panel and automation toolkit for dynamically adjusting your Antminer S9/S9i's power output based on room temperature from a UbiBot sensor.
Turns your miner into a <strong>smart heater</strong> that keeps your space warm, safe, and energy-efficient — all while earning Bitcoin.
</p>
<hr/>

<h2>📁 Folder Structure</h2>

<pre>
thermohash/
├── app/
│   ├── main.py               ← FastAPI server backend
│   ├── templates/
│   │   └── index.html        ← UI with live log view
│   ├── img/
│   │   └── logo.svg          ← Logo for Braiins/Bitcoin
│   └── config.ini            ← Log & working dir config
├── scripts/
│   ├── get-room-temp-ubibot.py
│   ├── thermohash.py
│   └── config.ini            ← Miner control + power mapping
├── last_power_target.json    ← Auto-generated cache
└── README.md                 ← This file
</pre>

<hr/>

<h2>⚙️ Setup & Requirements</h2>

<h3>🐍 Python Modules</h3>
<pre>
pip install fastapi uvicorn jinja2
</pre>

<h3>🧰 System Dependencies</h3>
<pre>
sudo apt install sshpass busybox
</pre>

<h3>🪟 Run the Web App</h3>
<pre>
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
</pre>

Then visit: <a href="http://localhost:8000" target="_blank">http://localhost:8000</a>

<hr/>

<h2>🧠 Smart Temperature-to-Power Mapping</h2>

<pre>
[temperature]
temp_to_power_mapping = {
    "5": 850,
    "10": 700,
    "15": 500,
    "20": 350
}
</pre>

<p>
→ Automatically defaults to <strong>350W</strong> for any temperature above 20°C.<br/>
→ Keeps your miner from overheating or running too cold.
</p>

<img src="https://media.giphy.com/media/fAnEC88LccN7a/giphy.gif" alt="Smart Miner Thinking" width="80%"/>

<hr/>

<h2>🧩 Configuration Files</h2>

<h3>📄 <code>app/config.ini</code></h3>
<pre>
[paths]
log_file = /absolute/path/to/logfile.log
working_dir = /absolute/path/to/scripts
</pre>

<h3>📄 <code>scripts/config.ini</code></h3>
<pre>
[miner]
hostname = 192.168.1.100
root_password = your_root_password

[temperature]
temp_to_power_mapping = {
    "5": 850,
    "10": 700,
    "15": 500,
    "20": 350
}
</pre>

<hr/>

<h2>⏱️ Add to Cron</h2>
<p>Automate temperature-based power adjustments every hour:</p>
<pre>
crontab -e
</pre>

<pre>
22 * * * * /usr/bin/python3 /path/to/scripts/get-room-temp-ubibot.py | xargs -r /usr/bin/python3 /path/to/scripts/thermohash.py >> /absolute/path/to/logfile.log 2>&1
</pre>

<p>
✔️ Auto-runs temperature fetch + power tuning<br/>
✔️ Logs results for web dashboard viewing
</p>

<hr/>

<h2>🖥️ Dashboard Features</h2>
<ul>
  <li>✨ Live-styled dark UI</li>
  <li>📜 View and scroll through log history</li>
  <li>🚀 One-click manual script trigger</li>
  <li>🎨 Bitcoin + Braiins branding ready</li>
</ul>

<img src="https://media.giphy.com/media/eNAsjO55tPbgaor7ma/giphy.gif" alt="Click Run Script" width="70%"/>

<hr/>

<h2>🛡️ Safety & Security</h2>
<ul>
  <li>✅ Never drops below 350W — safe for hashboards & PSU</li>
  <li>✅ Avoids SSH if power hasn't changed</li>
  <li>⚠️ You may wish to secure the web UI with a proxy, token, or VPN</li>
</ul>

<hr/>

<h2>🧑‍💻 Author Notes</h2>
<p>
This was built to automate hash tuning on a Braiins OS+ powered Antminer S9 for both home heating and mining optimization.
</p>

<p>
Pull requests welcome. Suggestions? Open an issue or <strong>fork and hash on</strong>.
</p>

<img src="https://media.giphy.com/media/l41lFw057lAJQMwg0/giphy.gif" alt="Mining Forever" width="60%"/>

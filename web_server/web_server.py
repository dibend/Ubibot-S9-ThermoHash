from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import configparser
import subprocess
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the img directory for serving images
app.mount("/img", StaticFiles(directory="img"), name="img")

# Load configuration
config = configparser.ConfigParser()
config.read("config.ini")

LOG_FILE = Path(config.get("paths", "log_file"))
WORKING_DIR = Path(config.get("paths", "working_dir"))
SCRIPT_PATH = WORKING_DIR / "thermohash.py"
TEMP_SCRIPT_PATH = WORKING_DIR / "get-room-temp-ubibot.py"

# Ensure log file exists
if not LOG_FILE.exists():
    with LOG_FILE.open("w") as f:
        f.write("Thermohash Log Initialized\n")

# Templates setup
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def read_log(request: Request):
    """Display the log file content in a web browser."""
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            log_content = f.read()
    else:
        log_content = "Log file not found."
    return templates.TemplateResponse(
        "index.html", {"request": request, "log_content": log_content}
    )


@app.post("/run-script")
async def run_script():
    """Run the script and append output to the log file."""
    try:
        with open(LOG_FILE, "a") as f:
            f.write("\n--- Running Thermohash Script ---\n")
            
            # Construct the command
            temp_command = ["python3", str(TEMP_SCRIPT_PATH)]
            
            try:
                temp_output = subprocess.check_output(temp_command, text=True).strip()
            except subprocess.CalledProcessError as e:
                f.write(f"\n--- Failed to get room temperature: {e} ---\n")
                return {"status": "Failed to get room temperature"}

            thermohash_command = ["python3", str(SCRIPT_PATH), temp_output]

            # Change working directory and run the script
            process = subprocess.Popen(
                thermohash_command,
                cwd=WORKING_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                f.write(stdout)
                f.write("\n--- Script Execution Complete ---\n")
            else:
                f.write(stderr)
                f.write(f"\n--- Script Execution Failed: Return code {process.returncode} ---\n")
                return {"status": "Script execution failed"}

    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"\n--- Script Execution Failed: {e} ---\n")
        return {"status": "Script execution failed"}

    return {"status": "Script executed successfully!"}

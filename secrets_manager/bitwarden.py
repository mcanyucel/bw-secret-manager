import subprocess
import json
import utils
import re
import os

def run_bw(args, session=None, capture_json=False):
    """Run a Bitwarden CLI command.

    Args:
        args (list): List of arguments for the Bitwarden CLI command.
        session (str, optional): Session token for authentication. Defaults to None.
        capture_json (bool, optional): Whether to parse the output as JSON. Defaults to False.

    Returns:
        str or dict: The command output as a string or parsed JSON object.
    """
    cmd = ["bw"] + args
    if session:
        cmd += ["--session", session]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if capture_json:
            return json.loads(result.stdout)
        else:
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        utils.error(f"Bitwarden command failed: {' '.join(cmd)}")
        utils.error(f"stderr: {e.stderr.strip()}")
        raise


def build_folder_map(session):
    folders = run_bw(["list", "folders"], session=session, capture_json=True)
    return {f["id"]: f["name"] for f in folders if f["id"] is not None}

def ensure_login():
    if not is_logged_in():
        email = input("Enter Bitwarden Email: ")
        # bw login will prompt for master password interactively
        subprocess.run(["bw", "login", email], check=True)
        utils.success(f"Logged in as {email}")
    else:
        utils.info("Already logged in, skipping login.")


def unlock_vault():
    utils.info("Unlocking vault...")
    if "BW_PASSWORD" not in os.environ:
        master_password = input("Enter Bitwarden Master Password: ")
        os.environ["BW_PASSWORD"] = master_password

    result = run_bw(["unlock", "--passwordenv", "BW_PASSWORD"], capture_json=False)    
    
    match = re.search(r'"([^"]+)"', result)
    if not match:
        raise RuntimeError("Could not parse session key from unlock output")
    session = match.group(1)

    utils.success("Vault unlocked, session acquired")
    return session



def lock_vault():
    run_bw(["lock"])
    utils.info("Vault locked.")

def get_bw_status():
    result = subprocess.run(["bw", "status"], capture_output=True, text=True)
    return json.loads(result.stdout)

def is_logged_in():
    status = get_bw_status()
    return status.get("status") != "unauthenticated"

def is_unlocked():
    status = get_bw_status()
    return status.get("status") == "unlocked"

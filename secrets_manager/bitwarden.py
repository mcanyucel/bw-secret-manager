import subprocess
import json
import sys
import utils

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
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        utils.error("Error running bw: " + result.stderr.strip())
        sys.exit(1)
    return json.loads(result.stdout) if capture_json else result.stdout.strip()

def ensure_login():
    status = run_bw(["status"], capture_json=True)
    if not status.get("loggedIn"):
        client_id = input("Enter Bitwarden Client ID: ").strip()
        client_secret = input("Enter Bitwarden Client Secret: ").strip()
        run_bw(["login", "--apikey", "--client-id", client_id, "--client-secret", client_secret])
        utils.success("Logged in to Bitwarden.")
        
def unlock_vault():
    utils.info("Unlocking vault...")
    return run_bw(["unlock", "--raw"])

def lock_vault():
    run_bw(["lock"])
    utils.info("Vault locked.")

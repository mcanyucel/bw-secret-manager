from pathlib import Path
import bitwarden
import utils

def parse_env_example(example_file="env.example"):
    env_vars = []
    with open(example_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                var_name = line.split("=", 1)[0].strip()
                env_vars.append(var_name)
    return env_vars


def fetch_secret(session, project, env, key, id_to_name):
    """Fetch a secret from Bitwarden folders.

    Args:
        session (str): Bitwarden session token.
        project (str): Project name.
        env (str): Environment name.
        key (str): Secret key.
        id_to_name (dict): Mapping of folder IDs to names.

    Returns:
        str: The secret value.
    """
    items = bitwarden.run_bw(["list", "items"], session=session, capture_json=True)
    target_folder = f"{project}/{env}"
    for item in items:
        if item.get("name") == key:
            folder_id = item.get("folderId")
            if id_to_name.get(folder_id) == target_folder:
                return item.get("notes") or item.get("login", {}).get("password")
    utils.warn(f"Warning: secret {key} not found in {target_folder}")
    return ""


import sys
from pathlib import Path
import bitwarden
import utils

def write_env_file(session, project, env, keys, id_to_name):
    """Write the .env file with secrets fetched from Bitwarden, showing inline progress."""
    tmpFile = Path(f".env.{env}.tmp")
    with open(tmpFile, "w") as f:
        for key in keys:
            secret = fetch_secret(session, project, env, key, id_to_name)
            if secret is not None:
                f.write(f"{key}={secret}\n")
            # Inline progress update (overwrite same line)
                sys.stdout.write(f"\r[INFO] saving {key} for {env}...\033[K")
                sys.stdout.flush()


    # Final newline so the last message doesn't stick on the same line
    sys.stdout.write("\n")
    tmpFile.replace(f".env.{env}")
    utils.success(f".env.{env} file written successfully.")
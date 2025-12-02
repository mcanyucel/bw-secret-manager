from pathlib import Path
import bitwarden
import utils

def parse_env_example(example_file="env.example"):
    """Parse the env.example file to get a list of environment variable names.

    Args:
        example_file (str): Path to the env.example file.

    Returns:
        list: List of environment variable names.
    """
    env_vars = []
    with open(example_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                var_name = line.split("=", 1)[0].strip()
                env_vars.append(var_name)
    return env_vars

def build_collection_map(session):
    """Build a mapping of collection names to their IDs in Bitwarden.

    Args:
        session (str): Bitwarden session token.
    Returns:
        dict: Mapping of collection names to IDs.
    """
    collections = bitwarden.run_bw(["list", "collections"], session=session, capture_json=True)
    return {c["id"]: c["name"] for c in collections}

def fetch_secret(session, project, env, key, id_to_name):
    """Fetch a secret from Bitwarden.
    
    Note:
        This function assumes that secrets are stored in collections named in the format "project/env/key".

    Args:
        session (str): Bitwarden session token.
        project (str): Project name.
        env (str): Environment name.
        key (str): Secret key.
        id_to_name (dict): Mapping of collection IDs to names.

    Returns:
        str: The secret value.
    """
    items = bitwarden.run_bw(["list", "items"], session=session, capture_json=True)
    target_collection = f"{project}/{env}"
    for item in items:
        if item.get("name") == key:
            for cid in item.get("collectionIds", []):
                if id_to_name.get(cid) == target_collection:
                    return item.get("notes") or item.get("login", {}).get("password")
    utils.warn(f"Warning: secret {key} not found in {target_collection}")
    return ""


def write_env_file(session, project, env, keys, id_to_name):
    """Write the .env file with secrets fetched from Bitwarden.

    Args:
        session (str): Bitwarden session token.
        project (str): Project name.
        env (str): Environment name.
        keys (list): List of environment variable names to fetch.
        id_to_name (dict): Mapping of collection IDs to names.
    """
    tmpFile = Path(f".env.{env}.tmp")
    with open(tmpFile, "w") as f:
        for key in keys:
            secret = fetch_secret(session, project, env, key, id_to_name)
            if secret is not None:
                f.write(f"{key}={secret}\n")
    tmpFile.replace(f".env.{env}")
    utils.success(f".env.{env} file written successfully.")

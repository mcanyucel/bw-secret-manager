import argparse
import bitwarden
import env_writer
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Fetch secrets from Bitwarden and generate .env files"
    )
    parser.add_argument(
        "--project",
        help="Project name (default: current folder name)",
        default=Path.cwd().name,
    )
    parser.add_argument(
        "--envs",
        nargs="+",
        help="Environments to fetch (default: dev prod)",
        default=["dev", "prod"],
    )
    parser.add_argument(
        "--example",
        help="Path to .env.example file (default: .env.example)",
        default=".env.example",
    )
    args = parser.parse_args()

    bitwarden.ensure_login()
    session = bitwarden.unlock_vault()
    keys = env_writer.parse_env_example(args.example)

    id_to_name = env_writer.build_collection_map(session)

    for env in args.envs:
        env_writer.write_env_file(session, args.project, env, keys, id_to_name)

    bitwarden.lock_vault()

if __name__ == "__main__":
    main()

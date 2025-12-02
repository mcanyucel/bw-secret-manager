# Secret Manager

A lightweight Python tool to fetch secrets from Bitwarden and generate environment files (`.env.dev`, `.env.prod`, etc.) based on the project's `.env.example` file.

## Features

- Uses Bitwarden CLI to securely fetch secrets.
- Supports multiple environments (development, production, etc.).
- Enforces a convention: secrets must be organized in Bitwarden collections named as `<project-name>/<environment>`.
- Generates environment files based on a provided example file.
- Writes generated files to a specified output directory atomically.
- Clear color-coded output for better readability.
- Provides a CLI entry point for easy integration into projects.

## Project Layout

When added to a project via Git subtree, the expected layout is as follows:

```bash
myproject/
  .env.example
  tools/
    secrets_manager/
      cli.py
      bitwarden.py
      env_writer.py
      utils.py
      pyproject.toml
```

## Prerequisites

- Python 3.8 or higher
- Bitwarden CLI installed and configured, with PATH set appropriately.

## Setup

Ensure you havea Bitwarden account and the Bitwarden CLI installed. Follow the instructions [here](https://bitwarden.com/help/article/cli/):

```bash
bw --version
```

### Option 1: Embedded as a Git Subtree

Add this repo as a subtree to your project:

```bash
git subtree add --prefix tools/secrets_manager https://github.com/yourusername/secrets_manager.git main --squash
```

Run directly:
```bash
python tools/secrets_manager/cli.py
```

### Option 2: Install as a Package

Install locally using pip:

```bash
pip install .
```

Now you can run the CLI using:

```bash
secret-manager --project myproject --envs dev prod --example .env.example
```

## Usage

1. Define the keys in your `.env.example` file:

```
DATABASE_URL=
REDIS_URL=
SECRET_KEY=
```

2. Organize your secrets in Bitwarden collections following the convention `<project-name>/<environment>`. For example, for a project named `myproject` and an environment `dev`, create a collection named `myproject/dev`.

3. Run the script:

#### A. Embedded

```bash
python tools/secrets_manager/cli.py
```

#### B. Installed Package

```bash
secret-manager
```

By default:

- Project name = current folder
- Environment = `dev` and `prod`
- Example file = `.env.example`

4. You can customize the behavior using command-line arguments:

```bash
python tools/secrets_manager/cli.py --project myapp --envs staging qa --example config/.env.template
```

## Workflow

1. Login: If not logged in, the script will prompt you to log in to Bitwarden.
2. Unlock: If your vault is locked, you'll be prompted to unlock it with your master password.
3. Fetch Secrets: The script fetches secrets from the specified Bitwarden collections.
4. Generate Files: It generates the environment files based on the `.env.example` file. 
5. Lock: The vault is locked again after fetching the secrets.

## Notes

- Ensure that your Bitwarden CLI is properly configured and that you have access to the necessary collections.
- Secrets are never stored in the repository; they are fetched at runtime.
- Handle your master password and session tokens securely.
- If a secret is missing, you will be notified in the output with a `[WARN]` message.

## Best Practices

- Always git-ignore your generated `.env.*` files to avoid committing sensitive information:

```
.env.*
```

- Store values in Notes or Password fields in Bitwarden items for better compatibility. Avoid using custom fields unless necessary.
- Regularly update your Bitwarden CLI to benefit from the latest features and security patches.
- Rotate your secrets periodically to enhance security.
- [WARN]s are signals, not blockers. 
- Avoid hardcoding sensitive information in your codebase.


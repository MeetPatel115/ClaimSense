"""Check the environment: Python, packages and .env settings."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Find .env in the project root (one level above src/), wherever you run from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)

problems = []

# 1. Python and environment
print("Python      :", sys.version.split()[0])
print("Environment :", sys.prefix)
if ".venv" not in sys.prefix:
    problems.append("Not running inside .venv. Activate it: .venv\\Scripts\\Activate.ps1")

# 2. Packages
try:
    import azure.identity
    import azure.storage.blob
    print("storage-blob:", azure.storage.blob.__version__)
    print("identity    :", azure.identity.__version__)
except ImportError as exc:
    problems.append(f"Missing package ({exc.name}). Run: pip install -r requirements.txt")

# 3. Settings from .env
print(".env file   :", ENV_FILE, "(found)" if ENV_FILE.exists() else "(NOT FOUND)")
if not ENV_FILE.exists():
    problems.append("Create .env in the project root (not inside src/).")

url = os.getenv("CLAIMSENSE_ACCOUNT_URL")
container = os.getenv("LANDING_CONTAINER")
folder = os.getenv("LANDING_FOLDER")
print("Account URL :", url)
print("Container   :", container)
print("Folder      :", folder)

if not url or "<" in url:
    problems.append("Set CLAIMSENSE_ACCOUNT_URL in .env to your real storage account URL.")
elif not (url.startswith("https://") and url.rstrip("/").endswith(".blob.core.windows.net")):
    problems.append("CLAIMSENSE_ACCOUNT_URL should look like https://<account>.blob.core.windows.net")

# Result
print()
if problems:
    print("Fix these:")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("Setup OK. Next: connect to the data lake.")
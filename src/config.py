"""Shared settings for all ClaimSense scripts."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

ACCOUNT_URL = os.getenv("CLAIMSENSE_ACCOUNT_URL", "").rstrip("/")
LANDING_CONTAINER = os.getenv("LANDING_CONTAINER", "landing")
LANDING_FOLDER = os.getenv("LANDING_FOLDER", "claims")
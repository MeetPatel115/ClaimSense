"""Step C: upload a single file to landing/claims/<today>/."""

import sys
from datetime import date
from pathlib import Path

from azure.storage.blob import ContentSettings

from config import LANDING_CONTAINER, LANDING_FOLDER
from connect import get_service

file_path = Path(sys.argv[1])                         # the file to upload, from the command line
blob_name = f"{LANDING_FOLDER}/{date.today().isoformat()}/{file_path.name}"

service = get_service()
blob = service.get_blob_client(container=LANDING_CONTAINER, blob=blob_name)

with file_path.open("rb") as data:                    # "rb": read bytes (PDFs aren't text)
    blob.upload_blob(
        data,
        overwrite=False,                              # never replace an existing file
        content_settings=ContentSettings(content_type="application/pdf"),
    )

print("Uploaded to:", blob.url)
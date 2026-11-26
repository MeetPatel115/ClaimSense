"""Step D: upload every PDF in a folder to landing/claims/<today>/, one by one."""

import argparse
import time
from datetime import date
from pathlib import Path

from azure.core.exceptions import HttpResponseError, ResourceExistsError
from azure.storage.blob import ContentSettings

from config import LANDING_CONTAINER, LANDING_FOLDER
from connect import get_service


# 1. Options from the command line
def read_options():
    parser = argparse.ArgumentParser(description="Upload PDFs to the landing zone one by one.")
    parser.add_argument("--folder", required=True, type=Path, help="local folder with the PDFs")
    parser.add_argument("--interval", type=float, default=15, help="seconds between files")
    parser.add_argument("--limit", type=int, help="only the first N files")
    parser.add_argument("--dry-run", action="store_true", help="list files, upload nothing")
    return parser.parse_args()


# 2. Find the PDFs, sorted so the order is predictable
def find_pdfs(folder: Path, limit: int | None) -> list[Path]:
    pdfs = sorted(f for f in folder.iterdir() if f.suffix.lower() == ".pdf")
    return pdfs[:limit] if limit else pdfs


# 3. File names already in landing/claims/ (any date), so re-runs skip them
def already_uploaded(service) -> set[str]:
    container = service.get_container_client(LANDING_CONTAINER)
    blobs = container.list_blobs(name_starts_with=f"{LANDING_FOLDER}/")
    return {b.name.split("/")[-1] for b in blobs}


# 4. Upload one file
def upload_one(service, pdf: Path, blob_name: str) -> None:
    blob = service.get_blob_client(container=LANDING_CONTAINER, blob=blob_name)
    with pdf.open("rb") as data:
        blob.upload_blob(
            data,
            overwrite=False,
            content_settings=ContentSettings(content_type="application/pdf"),
            metadata={"source": "claimsense_uploader"},
        )


# 5. Main loop
def main():
    opts = read_options()
    pdfs = find_pdfs(opts.folder, opts.limit)
    target = f"{LANDING_FOLDER}/{date.today().isoformat()}"
    print(f"{len(pdfs)} PDFs -> {LANDING_CONTAINER}/{target}/")

    if opts.dry_run:
        for pdf in pdfs:
            print("  would upload", pdf.name)
        return

    service = get_service()
    done = already_uploaded(service)
    uploaded = skipped = failed = 0

    for n, pdf in enumerate(pdfs, start=1):
        label = f"[{n}/{len(pdfs)}]"
        if pdf.name in done:
            skipped += 1
            print(label, "skipped ", pdf.name)
            continue
        try:
            upload_one(service, pdf, f"{target}/{pdf.name}")
            uploaded += 1
            print(label, "uploaded", pdf.name)
        except ResourceExistsError:
            skipped += 1
            print(label, "skipped ", pdf.name)
        except HttpResponseError as exc:          # one bad file doesn't stop the run
            failed += 1
            print(label, "FAILED  ", pdf.name, exc.status_code, exc.message)

        if n < len(pdfs):
            time.sleep(opts.interval)

    print(f"Done: {uploaded} uploaded, {skipped} skipped, {failed} failed.")


if __name__ == "__main__":
    main()
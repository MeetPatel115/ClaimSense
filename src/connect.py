"""Step B: connect to the data lake and list containers."""

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from config import ACCOUNT_URL


def get_service() -> BlobServiceClient:
    # DefaultAzureCredential uses your `az login` (no keys or passwords in code).
    credential = DefaultAzureCredential()
    return BlobServiceClient(account_url=ACCOUNT_URL, credential=credential)


if __name__ == "__main__":
    service = get_service()
    print("Connected to:", ACCOUNT_URL)
    for container in service.list_containers():
        print("  container:", container.name)
# ClaimSense

Event-driven insurance claims intake on Azure: claim documents land in ADLS Gen2,
get OCR'd by Document Intelligence, flow through a Delta Lake medallion architecture,
and feed Azure ML, Microsoft Foundry and Power BI.

## Setup
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
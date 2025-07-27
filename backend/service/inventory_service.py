import os
from fastapi import UploadFile
from backend.service.bill_analysis_service import analyze_bill

INVENTORY_DB = []  # In-memory for demo

def get_inventory():
    return INVENTORY_DB

def process_inventory_upload(file: UploadFile):
    # Save file temporarily
    contents = file.file.read()
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(contents)
    # Analyze bill
    details = analyze_bill(temp_path)
    INVENTORY_DB.append(details)
    os.remove(temp_path)
    return details

from fastapi import APIRouter, UploadFile, File
from backend.service.inventory_service import get_inventory, process_inventory_upload
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/view")
def view_inventory():
    inventory = get_inventory()
    return {"inventory": inventory}

@router.post("/upload")
def upload_inventory(file: UploadFile = File(...)):
    result = process_inventory_upload(file)
    return JSONResponse(content=result)

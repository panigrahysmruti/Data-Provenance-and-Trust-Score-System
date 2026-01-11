from fastapi import APIRouter , UploadFile , File
from core.hashing import generate_hash
from backend.database import insert_dataset



router = APIRouter()



@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_hash = generate_hash(file_bytes)

    # Store in DB
    insert_dataset(file.filename, file_hash)

    return {
        "filename": file.filename,
        "hash": file_hash,
        "stored": True
    }

from fastapi import APIRouter, UploadFile, File
from core.hashing import generate_hash
from backend.database import insert_dataset, get_hash_by_filename

router = APIRouter()


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_hash = generate_hash(file_bytes)

    # 🔒 Check if dataset already exists
    existing_hash = get_hash_by_filename(file.filename)
    if existing_hash is not None:
        return {
            "filename": file.filename,
            "status": "ALREADY_EXISTS",
            "message": "Dataset already uploaded. Use verify instead."
        }

    # Store only if first-time upload
    insert_dataset(file.filename, file_hash)

    return {
        "filename": file.filename,
        "hash": file_hash,
        "stored": True
    }


@router.post("/verify")
async def verify_dataset(file: UploadFile = File(...)):
    file_bytes = await file.read()
    current_hash = generate_hash(file_bytes)

    stored_hash = get_hash_by_filename(file.filename)

    if stored_hash is None:
        return {
            "filename": file.filename,
            "status": "NOT_FOUND",
            "message": "Dataset not found in database"
        }

    if current_hash == stored_hash:
        return {
            "filename": file.filename,
            "status": "AUTHENTIC",
            "message": "Dataset integrity verified"
        }

    return {
        "filename": file.filename,
        "status": "TAMPERED",
        "message": "Dataset hash mismatch detected"
    }

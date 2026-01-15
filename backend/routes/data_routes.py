from fastapi import APIRouter, UploadFile, File
from core.hashing import generate_hash
from core.tamper_detection import detect_tampering
from backend.database import (
    insert_dataset,
    get_dataset_by_filename,
    get_hash_by_dataset_id
)

router = APIRouter()


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_hash = generate_hash(file_bytes)

    existing = get_dataset_by_filename(file.filename)

    if existing is not None:
        return {
            "filename": file.filename,
            "status": "UPLOAD_LOCKED",
            "message": "Dataset already uploaded. Upload is locked. Use verify."
        }

    dataset_id = insert_dataset(file.filename, file_hash)

    return {
        "dataset_id": dataset_id,
        "filename": file.filename,
        "hash": file_hash,
        "stored": True
    }


@router.post("/verify")
async def verify_dataset(file: UploadFile = File(...)):
    file_bytes = await file.read()
    current_hash = generate_hash(file_bytes)

    dataset = get_dataset_by_filename(file.filename)

    if dataset is None:
        return {
            "filename": file.filename,
            "status": "NOT_FOUND",
            "message": "Dataset not found. Upload first."
        }

    dataset_id, original_hash = dataset

    is_tampered = detect_tampering(original_hash, current_hash)

    if is_tampered:
        return {
            "filename": file.filename,
            "status": "TAMPERED",
            "message": "Dataset has been modified"
        }

    return {
        "filename": file.filename,
        "status": "AUTHENTIC",
        "message": "Dataset integrity verified"
    }

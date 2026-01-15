def detect_tampering(original_hash: str, current_hash: str) -> bool:
    """
    Returns True if dataset is tampered
    """
    return original_hash != current_hash

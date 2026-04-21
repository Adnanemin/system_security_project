import hashlib

def commit_hash(bid, salt):
    data = f"{bid}:{salt}"
    return hashlib.sha256(data.encode()).hexdigest()
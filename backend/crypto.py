import hashlib

def commit_hash(bid, salt):
    data = f"{bid}:{salt}"
    return hashlib.sha256(data.encode()).hexdigest()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
# secure_doc.py
import json
import base64
import hashlib
import itertools
from typing import Dict, Tuple

def derive_key(password: str) -> bytes:
    """Simple KDF using SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).digest()

def xor_encrypt(data: bytes, key_bytes: bytes) -> bytes:
    """XOR data with repeating keystream."""
    return bytes(b ^ k for b, k in zip(data, itertools.cycle(key_bytes)))

def encrypt_meta(meta: Dict, password: str) -> str:
    raw_bytes = json.dumps(meta, ensure_ascii=True).encode("utf-8")
    keystream = derive_key(password)
    cipher_bytes = xor_encrypt(raw_bytes, keystream)
    return base64.b64encode(cipher_bytes).decode("ascii")

def decrypt_meta(encoded: str, password: str) -> Dict:
    cipher_bytes = base64.b64decode(encoded)
    plain_bytes = xor_encrypt(cipher_bytes, derive_key(password))
    return json.loads(plain_bytes.decode("utf-8"))

def save_secure_doc(path: str, text: str, meta: Dict, password: str):
    doc_obj = {
        "text": text,
        "meta_hidden": encrypt_meta(meta, password)
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc_obj, f, ensure_ascii=True, indent=2)

def load_secure_doc(path: str, password: str) -> Tuple[str, Dict]:
    with open(path, "r", encoding="utf-8") as f:
        doc_obj = json.load(f)
    text = doc_obj["text"]
    meta = decrypt_meta(doc_obj["meta_hidden"], password)
    return text, meta

if __name__ == "__main__":
    document_text = "This is a public section of the document."
    metadata_info = {"author":"Lior","created":"2025-09-23","department":"R&D"}
    secret_password = "super-secret-key"

    save_secure_doc("secure_doc.json", document_text, metadata_info, secret_password)
    loaded_text, loaded_meta = load_secure_doc("secure_doc.json", secret_password)

    print(loaded_text)
    print(loaded_meta)

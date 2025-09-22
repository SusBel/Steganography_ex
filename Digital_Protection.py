# sha256_demo_alt.py
import hashlib

def compute_sha256(text: str) -> str:
    """Return the SHA-256 hash of the given text as a hex string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

if __name__ == "__main__":
    original = "The quick brown fox"
    modified = "The quick brown f0x"  # small change

    hash_original = compute_sha256(original)
    hash_modified = compute_sha256(modified)

    print(f"Original text: {original}")
    print(f"Hash: {hash_original}\n")
    print(f"Modified text: {modified}")
    print(f"Hash: {hash_modified}")

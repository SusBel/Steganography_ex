# chaff_winnow_alt.py
import hmac
import hashlib
import random
from typing import List, Tuple

def compute_mac(data: bytes, secret: bytes) -> bytes:
    """Return HMAC-SHA256 tag for a piece of data."""
    return hmac.new(secret, data, hashlib.sha256).digest()

def generate_packets(msg: bytes, secret: bytes, block_size: int = 4, fake_ratio: float = 1.0) -> List[Tuple[bytes, bytes]]:
    rng = random.Random(2025)
    blocks = [msg[i:i+block_size] for i in range(0, len(msg), block_size)]
    
    genuine = [(b, compute_mac(b, secret)) for b in blocks]
    
    fake_blocks = []
    for _ in range(int(len(genuine) * fake_ratio)):
        fake_piece = rng.randbytes(block_size)
        fake_tag = rng.randbytes(32)
        fake_blocks.append((fake_piece, fake_tag))
    
    all_packets = genuine + fake_blocks
    rng.shuffle(all_packets)
    return all_packets

def extract_message(packets: List[Tuple[bytes, bytes]], secret: bytes) -> bytes:
    recovered = []
    for piece, tag_val in packets:
        if hmac.compare_digest(tag_val, compute_mac(piece, secret)):
            recovered.append(piece)
    return b"".join(recovered)

if __name__ == "__main__":
    shared_key = b"top-secret-key"
    secret_msg = b"Hidden treasure inside!"
    
    packets = generate_packets(secret_msg, shared_key, block_size=5, fake_ratio=1.5)
    original_msg = extract_message(packets, shared_key)
    
    print("Recovered message:", original_msg)

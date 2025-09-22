# selective_encrypt_alt.py
import re

def caesar_cipher(data: str, k: int = 5) -> str:
    def shift_char(c):
        if c.isdigit():
            return str((int(c) + k) % 10)
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            return chr((ord(c) - base + k) % 26 + base)
        return c
    return ''.join(map(shift_char, data))

# Regex for IDs (9–10 digits) and credit cards (13–19 digits)
SENSITIVE_RULES = [
    re.compile(r'\b\d{9,10}\b'),
    re.compile(r'\b\d{13,19}\b')
]

def protect(text: str, cipher=caesar_cipher) -> str:
    for rule in SENSITIVE_RULES:
        text = rule.sub(lambda m: cipher(m.group()), text)
    return text

if __name__ == "__main__":
    demo = "Customer: Jane Roe, ID 987654321, Card 4111111111111111."
    print(protect(demo))

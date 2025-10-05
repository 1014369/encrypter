# keypad_cipher.py
# Simple phone keypad cipher

# Key mapping
keypad = {
    'A': '21', 'B': '22', 'C': '23',
    'D': '31', 'E': '32', 'F': '33',
    'G': '41', 'H': '42', 'I': '43',
    'J': '51', 'K': '52', 'L': '53',
    'M': '61', 'N': '62', 'O': '63',
    'P': '71', 'Q': '72', 'R': '73', 'S': '74',
    'T': '81', 'U': '82', 'V': '83',
    'W': '91', 'X': '92', 'Y': '93', 'Z': '94',
    ' ': '00'
}

# Reverse map
reverse_keypad = {v: k for k, v in keypad.items()}

def encrypt_keypad(plaintext: str) -> str:
    """Encrypt plaintext to numeric keypad code."""
    result = []
    for ch in plaintext.upper():
        if ch in keypad:
            result.append(keypad[ch])
        elif ch == '\n':
            result.append('00')
        else:
            result.append('00')  # unknown = space
    return ' '.join(result)

def decrypt_keypad(ciphertext: str) -> str:
    """Decrypt numeric keypad string back to text."""
    parts = ciphertext.split()
    result = []
    for p in parts:
        result.append(reverse_keypad.get(p, '?'))
    return ''.join(result)

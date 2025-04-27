# --------------- [FULL CODE] Mini-AES 16-bit Encryption/Decryption ---------------

# S-Box dan Inverse S-Box
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}
INV_S_BOX = {v: k for k, v in S_BOX.items()}

# Fungsi dasar (sama seperti sebelumnya)
def gf_mul(a, b):
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        carry = a & 0x8
        a <<= 1
        if carry:
            a ^= 0x13
        b >>= 1
    return p & 0xF

def int_to_nibbles(val):
    return [(val >> 12) & 0xF, (val >> 8) & 0xF, (val >> 4) & 0xF, val & 0xF]

def nibbles_to_int(nibbles):
    return (nibbles[0] << 12) | (nibbles[1] << 8) | (nibbles[2] << 4) | nibbles[3]

def sub_nibbles(state):
    return [S_BOX[n] for n in state]

def shift_rows(state):
    return [state[0], state[1], state[3], state[2]]

def mix_columns(state):
    return [
        gf_mul(1, state[0]) ^ gf_mul(4, state[2]),
        gf_mul(1, state[1]) ^ gf_mul(4, state[3]),
        gf_mul(4, state[0]) ^ gf_mul(1, state[2]),
        gf_mul(4, state[1]) ^ gf_mul(1, state[3])
    ]

def add_round_key(state, key):
    return [s ^ k for s, k in zip(state, key)]

def key_expansion(master_key):
    w = [0]*6
    w[0] = (master_key >> 12) & 0xF
    w[1] = (master_key >> 8) & 0xF
    w[2] = (master_key >> 4) & 0xF
    w[3] = master_key & 0xF

    RCON1 = 0x3
    RCON2 = 0x6

    w[4] = w[0] ^ S_BOX[w[3]] ^ RCON1
    w[5] = w[1] ^ w[4]

    round_keys = [
        [w[0], w[1], w[2], w[3]],
        [w[4], w[5], w[2] ^ w[4], w[3] ^ w[5]],
        [w[4] ^ S_BOX[w[3] ^ w[5]], w[5] ^ S_BOX[w[2] ^ w[4]], w[2] ^ w[4], w[3] ^ w[5]]
    ]
    return round_keys

# --------------- ENKRIPSI ---------------
def encrypt(plaintext, master_key):
    state = int_to_nibbles(plaintext)
    round_keys = key_expansion(master_key)
    
    state = add_round_key(state, round_keys[0])
    
    for round_num in range(1, 3):
        state = sub_nibbles(state)
        state = shift_rows(state)
        if round_num != 2:
            state = mix_columns(state)
        state = add_round_key(state, round_keys[round_num])
    
    return nibbles_to_int(state)

# --------------- DEKRIPSI ---------------
def inv_mix_columns(state):
    return [
        gf_mul(9, state[0]) ^ gf_mul(2, state[2]),
        gf_mul(9, state[1]) ^ gf_mul(2, state[3]),
        gf_mul(2, state[0]) ^ gf_mul(9, state[2]),
        gf_mul(2, state[1]) ^ gf_mul(9, state[3])
    ]

def inv_sub_nibbles(state):
    return [INV_S_BOX[n] for n in state]

def inv_shift_rows(state):
    return [state[0], state[1], state[3], state[2]]

def decrypt(ciphertext, master_key):
    state = int_to_nibbles(ciphertext)
    round_keys = key_expansion(master_key)
    
    # Round 2
    state = add_round_key(state, round_keys[2])
    state = inv_shift_rows(state)
    state = inv_sub_nibbles(state)
    
    # Round 1
    state = add_round_key(state, round_keys[1])
    state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_nibbles(state)
    
    # Final
    state = add_round_key(state, round_keys[0])
    
    return nibbles_to_int(state)

# --------------- MAIN PROGRAM ---------------
def main():
    # Input handling yang lebih robust
    try:
        plaintext = input("Masukkan 2 huruf plaintext (contoh 'AB'): ")
        if len(plaintext) != 2:
            raise ValueError("Harus 2 karakter!")
        plaintext_int = ord(plaintext[0]) << 8 | ord(plaintext[1])
        
        key = input("Masukkan key (4 digit hex, contoh '1A2B'): ")
        if len(key) != 4 or not all(c in '0123456789ABCDEF' for c in key.upper()):
            raise ValueError("Key harus 4 digit hex!")
        key_int = int(key, 16)
        
        # Enkripsi
        ciphertext = encrypt(plaintext_int, key_int)
        print(f"\nCiphertext (hex): {hex(ciphertext)}")
        
        # Dekripsi
        decrypted = decrypt(ciphertext, key_int)
        decrypted_text = chr(decrypted >> 8) + chr(decrypted & 0xFF)
        print(f"Hasil Dekripsi: {decrypted_text}")
    
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
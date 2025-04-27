# Mini-AES 16-bit menerima input huruf
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

def gf_mul(a, b):
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        carry = a & 0x8
        a <<= 1
        if carry:
            a ^= 0x13  # GF(2^4) irreducible polynomial
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
        [w[4] ^ w[2] ^ w[4], w[5] ^ w[3] ^ w[5], w[2] ^ w[4] ^ w[4], w[3] ^ w[5] ^ w[5]],
        [0, 0, 0, 0]
    ]
    return round_keys

def encrypt(plaintext, master_key):
    steps = []
    state = int_to_nibbles(plaintext)
    round_keys = key_expansion(master_key)

    steps.append(f"Initial State: {state}")

    state = add_round_key(state, round_keys[0])
    steps.append(f"After AddRoundKey (Round 0): {state}")

    for round_num in range(1, 4):
        state = sub_nibbles(state)
        steps.append(f"After SubNibbles (Round {round_num}): {state}")

        state = shift_rows(state)
        steps.append(f"After ShiftRows (Round {round_num}): {state}")

        if round_num != 3:
            state = mix_columns(state)
            steps.append(f"After MixColumns (Round {round_num}): {state}")

        state = add_round_key(state, round_keys[round_num-1])
        steps.append(f"After AddRoundKey (Round {round_num}): {state}")

    ciphertext = nibbles_to_int(state)
    return ciphertext, steps

# ---------------- Main Program ----------------

plaintext_input = input("Masukkan 2 huruf plaintext (contoh 'AB'): ")
key_input = input("Masukkan key (4 karakter hex, contoh '1A2B'): ")

if len(plaintext_input) != 2:
    print("Error: Harus 2 huruf saja!")
else:
    plaintext = (ord(plaintext_input[0]) << 8) | ord(plaintext_input[1])
    key = int(key_input, 16)

    ciphertext, steps = encrypt(plaintext, key)

    print("\n--- Proses Enkripsi ---")
    for step in steps:
        print(step)

    print("\nCiphertext (hex):", hex(ciphertext))

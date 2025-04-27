# S-Box untuk key expansion
S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

# Fungsi rotasi untuk key expansion
def rotate_left(nibbles):
    return nibbles[1:] + [nibbles[0]]

# Fungsi untuk menambahkan round key menggunakan XOR
def add_round_key(state, round_key):
    return [state[i] ^ round_key[i] for i in range(len(state))]

# Fungsi untuk key expansion
def key_expansion(master_key):
    round_keys = []

    # Memecah kunci utama 16-bit menjadi 4 nibble
    round_keys.append([master_key >> 12 & 0xF, master_key >> 8 & 0xF, master_key >> 4 & 0xF, master_key & 0xF])

    # Proses key expansion untuk ronde-ronde selanjutnya
    for i in range(3):  # Menghasilkan 3 round keys tambahan
        # Mengambil 4 nibble terakhir dari round key sebelumnya
        temp = round_keys[i]
        
        # Rotasi dan substitusi S-Box untuk nibble pertama
        temp = rotate_left(temp)
        temp = [S_BOX[x] for x in temp]
        
        # XOR dengan round constant untuk membingungkan key expansion
        temp[0] ^= 0x1  # Round constant (sederhana hanya XOR dengan 1)

        # Generate round key untuk ronde berikutnya
        next_round_key = [round_keys[i][j] ^ temp[j] for j in range(4)]
        round_keys.append(next_round_key)
    
    return round_keys

# Fungsi untuk mengonversi integer ke dalam bentuk nibbles
def int_to_nibbles(val):
    return [val >> 12 & 0xF, val >> 8 & 0xF, val >> 4 & 0xF, val & 0xF]

# Fungsi untuk mengonversi nibbles kembali ke dalam bentuk integer
def nibbles_to_int(nibbles):
    return (nibbles[0] << 12) | (nibbles[1] << 8) | (nibbles[2] << 4) | nibbles[3]

# Contoh Penggunaan Key Expansion
def main():
    key_input = 0x1A2B  # Kunci utama 16-bit
    round_keys = key_expansion(key_input)
    
    print("Round Keys:")
    for idx, key in enumerate(round_keys):
        print(f"Round {idx} Key: {key} ({nibbles_to_int(key):#06x})")

if __name__ == "__main__":
    main()

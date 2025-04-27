# project_ets_kripto

#Flowchart Mini-AES
Start
  ↓
Input Plaintext (16-bit) & Key (16-bit)
  ↓
Convert Plaintext to 4 Nibbles
  ↓
Key Expansion → Generate Round Keys
  ↓
Initial AddRoundKey (state XOR RoundKey0)
  ↓
[Repeat 3 Rounds]
    ├─ SubNibbles (Substitusi S-Box)
    ↓
    ├─ ShiftRows (Tukar posisi nibble)
    ↓
    ├─ If NOT Final Round:
    │    └─ MixColumns (Multiplikasi GF(2⁴))
    ↓
    ├─ AddRoundKey (state XOR RoundKey)
  ↑
[End Repeat after 3 Rounds]
  ↓
Convert 4 Nibbles to Ciphertext (16-bit)
  ↓
Output Ciphertext
  ↓
End

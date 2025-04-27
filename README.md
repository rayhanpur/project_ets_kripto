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

#Testcase 1
Input: BC
Key: E135 (1110000100110101)
Cyphertext: 0111000010100011 (bit)
Cyphertext: 0x70a3 (hex)

#Testcase 2
Input: AB
Key: AF0C (1010111100001100)
Cyphertext: 0110011110000100 (bit)
Cyphertext: 0x6784 (hex)

#Testcase 3
Input: DA
Key: 5C33 (1110000100110101)
Cyphertext: 0100001001000111 (bit)
Cyphertext: 0x4247 (hex)

#Analisis Kelebihan dan Keterbatasan dari mini-AES
Kelebihan:
- Mini-AES ini lebih sederhana daripada algoritma AES yang lebih besar seperti AES_128 tang dimana dapat diimplementasikan dan dipahami dengan lebih mudah.
- Mini-AES cocok untuk dipake belajar, dikarenakan kesederhanaannya jadi mebih mudah untuk mempelajari algoritmanya dan untuk mempelajari konsep kriptografi simetris.
- Mini-AES ini lebih efisien untuk sistem yang memiliki sumber daya terbatas dikarenakan menggunakan bit yang kecil.

Kekurangan:
- Mini-AES kurang aman buat dipake karena cuman menggunakan 16-bit untuk plaintext dan key yang dimana mini-AES mudah untuk di bruteforce.
- Mini-AES hanya memiliki 3 ronde yang dimana sangat sedikit sehingga mudah dianalisis oleh pihak ketiga yang ingin nge-attack.
- Keamanan Mini-AES yang hanya menggunakan 16 bit untuk membuat struktur dasar algoritmanya (seperti untuk S-box) yang dimana masih mudah untuk dianalisis oleh pihak ketiga.


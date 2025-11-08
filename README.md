# 🏆 CyCTF 2025 Qualifications - Symmetric Challenge Writeup

## 🔗 Overview

This repository contains the solution and writeup for the **Symmetric** cryptography challenge from the CyCTF 2025 Qualifications. The challenge involved exploiting a **CBC Padding Oracle vulnerability** to recover the encrypted flag.

## 💡 The Vulnerability

The challenge provided a service that used **AES in CBC mode** with an unknown, constant key and IV. The key flaw was in the decryption handler, which implicitly acted as a **Padding Oracle**. By sending specially crafted ciphertexts, we could determine if the resulting plaintext had valid PKCS#7 padding, allowing us to systematically decrypt the flag blocks byte by byte.

## 🛠 Solution Structure

The exploit was conducted in multiple phases, each corresponding to a Python script in this repository:

| Script | Purpose | Technique |
| :--- | :--- | :--- |
| `player.py` | **Challenge Code** | Original challenge source (for reference). |
| `solve2.py` | **Initial Oracle Test** | Confirmed the padding oracle and devised a method to bypass the "cheating" detection by modifying the last byte of the preceding ciphertext block. |
| `solve3.py` | **IV and Block Recovery** | Used the oracle to first recover the Intermediate State ($I_{aa}$), then successfully determined the **Initialization Vector (IV)**. With the IV, a full Padding Oracle attack was used to recover $P_0$ (the first flag block) and almost all of $P_1$ and $P_2$. |
| `solve4.py` | **Final Flag Assembly** | Used the challenge's **Encryption Oracle** to brute-force the two missing hexadecimal digits that could not be recovered by the padding oracle. |

---

## 🚀 Step-by-Step Breakdown

### 1. Initial Access and Padding Bypass (`solve2.py`)

We confirmed the Padding Oracle by iterating through all 256 possibilities for the last byte of the first ciphertext block ($C_0$) while attempting to decrypt $C_1$. This successfully found a byte that allowed the decryption to pass the padding check, confirming the exploit path.

### 2. IV Recovery and Full Decryption (`solve3.py`)

1.  **Intermediate State:** First, a padding oracle attack was run on a known block (all 'aa's) to determine the intermediate decryption state $I_{aa}$.
2.  **IV Calculation:** The same known block was then decrypted using the challenge's IV as the preceding block, giving us $P_{aa} = I_{aa} \oplus IV$. This allowed us to calculate the **IV**.
3.  **Block Decryption:** With the known IV, a full padding oracle attack was executed against $C_0$, $C_1$, and $C_2$, recovering most of the flag plaintext.

### 3. Brute-Forcing Completion (`solve4.py`)

The padding oracle attack inherently leaves the last byte of the original plaintext ambiguous. The flag was missing two hex digits:
`CyCTF{8817602d8**?**9c72ea815d3e34a**?**4292afb5a3e3ae}`

The script used the challenge's encryption oracle to re-encrypt the partially guessed flag, comparing the generated ciphertext blocks ($C'_0$ and $C'_1$) against the original blocks ($C_0$ and $C_1$) to determine the correct missing characters.

* `1st ?` was found to be `5`
* `2nd ?` was found to be `4`

---

## 🏁 Final Flag
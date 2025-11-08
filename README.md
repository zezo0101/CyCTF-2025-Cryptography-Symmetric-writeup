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
| `solve.py` | **Initial Block Decryption** | Confirmed the padding oracle and successfully decrypted the **last flag block** ($P_2$) using $C_1$ as the preceding block. |
| `solve2.py` | **Oracle Confirmation & Bypass** | Detailed confirmation of the padding oracle and development of the systematic bypass for the "cheating" detection. |
| `solve3.py` | **IV and Block Recovery** | Used the oracle to first recover the Intermediate State ($I_{aa}$), then determined the **Initialization Vector (IV)**. With the IV, a full Padding Oracle attack was used to recover $P_0$ (the first flag block) and most of $P_1$ and $P_2$. |
| `solve4.py` | **Final Flag Assembly** | Used the challenge's **Encryption Oracle** to brute-force the two missing hexadecimal digits that could not be recovered by the padding oracle. |

---

## 🚀 Step-by-Step Breakdown

### 1. Decrypting the Last Block (`solve.py`)

The first step was to successfully decrypt the last flag block ($P_2$) using the padding oracle.

* **Goal:** Recover the plaintext of the last ciphertext block ($C_2$).
* **Method:** We sent the ciphertext $C_1' \cdot C_2$, where $C_1'$ is $C_1$ with its last byte modified to `aa`. This modification successfully bypassed the cheating detection and allowed the decryption of $P_2$.
* **Result:** The decryption revealed the content of the last flag block: `4292afb5a3e3ae}` (plus the padding byte).

### 2. Oracle Confirmation and Systematic Bypass (`solve2.py`)

The next step refined the attack to systematically recover the rest of the flag blocks.

* **Method:** This script developed the systematic approach by iterating through all 256 possibilities for the last byte of the *preceding* ciphertext block to find the successful padding byte, which is necessary for a full oracle attack.

### 3. IV Recovery and Full Decryption (`solve3.py`)

To fully decrypt the flag, especially the first block ($P_0$), the Initialization Vector (IV) was required.

1.  **Intermediate State:** A padding oracle attack was run on a known block (all 'aa's) to determine the intermediate decryption state $I_{aa}$.
2.  **IV Calculation:** The same known block was then decrypted using the challenge's IV as the preceding block, giving us $P_{aa} = I_{aa} \oplus IV$. This allowed us to calculate the **IV**.
3.  **Block Decryption:** With the known IV, a full padding oracle attack was executed against $C_0$, $C_1$, and $C_2$, recovering most of the flag plaintext, resulting in:
    * `CyCTF{8817602d8?`
    * `9c72ea815d3e34a?`

### 4. Brute-Forcing Completion (`solve4.py`)

The flag was missing two hex digits due to the nature of the padding oracle attack.

The script used the challenge's encryption oracle to re-encrypt the partially guessed flag, comparing the generated ciphertext blocks ($C'_0$ and $C'_1$) against the original blocks ($C_0$ and $C_1$) to determine the correct missing characters.

* `1st ?` was found to be `5`
* `2nd ?` was found to be `4`

---

## 🏁 Final Flag CyCTF{8817602d859c72ea815d3e34a44292afb5a3e3ae}

## 🧑‍💻 Author

Wrote by: zeyad_0101

* Email: zeyadsheeref@gmail.com
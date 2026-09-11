<div align="center">

<img src="assets/README-banner.svg" width="100%" alt="AES Encryption Project" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&pause=900&color=8B7CFF&center=true&vCenter=true&width=820&lines=Encrypt+%E2%80%A2+Protect+%E2%80%A2+Decrypt;AES+Cryptography+Lab;Desktop+Security+Utility;Python+%2B+PyCryptodome+%2B+Tkinter" alt="Typing animation" />

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![AES](https://img.shields.io/badge/Cryptography-AES-8B7CFF?style=for-the-badge)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-42E8A3?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)

### 🔐 A Desktop Cryptography Learning Project

**A Python GUI for experimenting with AES-based text and file encryption workflows.**

</div>

---

## 🧠 Overview

AES Encryption Project is a desktop application built with Python and Tkinter to demonstrate symmetric encryption, password-based key handling, file processing and a security-focused GUI.

> **Educational project:** useful for learning cryptography concepts; not a replacement for audited encryption software or a production key-management system.

## ✨ Features

- 🔒 AES-based text encryption/decryption
- 📂 File encryption workflow
- 🔑 Password-based key handling
- 📈 File-processing progress display
- 🖥️ Tkinter desktop interface
- ✅ Input validation and error handling
- 📋 Copy encrypted/decrypted output

## ⚡ Workflow

```mermaid
flowchart LR
 A[Text / File] --> B[Password]
 B --> C[Key Handling]
 C --> D[AES Encryption]
 D --> E[Protected Output]
 E --> F[AES Decryption]
 F --> G[Original Data]
```

## 🛠️ Technology Stack

`Python` `Tkinter` `PyCryptodome` `AES` `File Handling`

## 📁 Project Structure

```text
AES-Encryption-Project/
├── aes_project.py
├── .gitignore
├── assets/
│   └── README-banner.svg
└── README.md
```

## 🚀 Quick Start

```bash
git clone https://github.com/wwwsahilchand123-maker/AES-Encryption-Project.git
cd AES-Encryption-Project
pip install pycryptodome
python aes_project.py
```

## 🔐 Security Roadmap

- [ ] Use Argon2id, scrypt or PBKDF2 with a random salt for password-derived keys
- [ ] Prefer authenticated encryption such as AES-GCM
- [ ] Detect ciphertext tampering with authentication tags
- [ ] Define a versioned encrypted-file format
- [ ] Add automated round-trip and wrong-password tests
- [ ] Add large-file and failure-recovery tests

## 🧪 Test Principle

```text
original data
    ↓ encrypt
ciphertext
    ↓ decrypt with same key
original data
```

Wrong passwords and modified ciphertext should fail safely.

## ⚠️ Security Note

Do not use this project to protect high-value real-world secrets until its cryptographic design and implementation have been independently reviewed and hardened.

---

<div align="center">

### 🔐 UNDERSTAND THE PRIMITIVE · RESPECT THE THREAT MODEL

**Built by Sahil Chand**

</div>

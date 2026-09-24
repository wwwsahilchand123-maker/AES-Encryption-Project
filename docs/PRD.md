# Product Requirements Document — AES Encryption Project

## 1. Product Overview
A desktop encryption utility for securely encrypting and decrypting text and files using password-based AES encryption.

## 2. Problem Statement
Users need a simple local workflow for protecting sensitive files and text without requiring command-line cryptography knowledge.

## 3. Target Users
- Students learning applied cryptography
- Users needing local file protection
- Developers studying secure encryption workflows

## 4. Core Features
- AES-256 encryption/decryption
- Password-based key derivation
- Text encryption
- File encryption/decryption
- Password-strength feedback
- GUI workflow

## 5. Functional Requirements
- Derive keys from passwords using PBKDF2.
- Generate a fresh random salt and IV/nonce for encryption.
- Correctly handle padding and binary file data.
- Decryption must reject invalid or tampered ciphertext.
- Preserve round-trip correctness for text and files.

## 6. Non-Functional Requirements
- Local-first operation
- Clear error messages
- Deterministic automated tests where applicable
- No plaintext password persistence

## 7. Security Requirements
- Never hard-code encryption keys.
- Never reuse a fixed IV.
- Use cryptographically secure randomness.
- Do not log plaintext or passwords.
- Treat authentication/integrity failures as security errors.

## 8. User Flow
Select operation → enter password → choose text/file → encrypt/decrypt → show result → save output.

## 9. Success Criteria
- Encryption/decryption round trips pass automated tests.
- Repeated encryption produces independent ciphertext.
- Incorrect passwords and malformed ciphertext fail safely.

## 10. Future Scope
- Authenticated encryption
- Key-file support
- Drag-and-drop files
- Secure key/password management

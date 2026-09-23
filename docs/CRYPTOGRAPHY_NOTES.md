# AES Encryption Notes

## Design
The project uses AES-256 for symmetric encryption and derives key material from a password with PBKDF2. A fresh salt and nonce/IV should be generated for each encryption operation.

## Password handling
Passwords are inputs to key derivation, not encryption keys stored by the application. Password strength checks improve usability but do not replace secure key derivation.

## Integrity
Decryption must reject altered ciphertext or authentication data. Tests should cover wrong passwords, modified ciphertext, and normal text/file round trips.

## File safety
Encrypted output should be written without accidentally retaining plaintext padding or mixing text and binary handling.

## Testing rule
Any cryptographic change should include a successful round-trip test and at least one failure-path test.

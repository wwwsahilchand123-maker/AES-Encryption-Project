from pathlib import Path
import tempfile

from aes_project import TextEncryption, FileEncryption


def test_text_round_trip():
    encryptor = TextEncryption("test-password")
    plaintext = "AES round-trip test"
    ciphertext = encryptor.encrypt(plaintext)
    assert ciphertext
    assert encryptor.decrypt(ciphertext) == plaintext


def test_text_wrong_password_fails_closed():
    ciphertext = TextEncryption("correct-password").encrypt("secret message")
    assert ciphertext
    assert TextEncryption("wrong-password").decrypt(ciphertext) is None


def test_text_tampering_fails_closed():
    ciphertext = TextEncryption("test-password").encrypt("integrity check")
    assert ciphertext
    tampered = ciphertext[:-2] + ("A" if ciphertext[-2] != "A" else "B") + ciphertext[-1]
    assert TextEncryption("test-password").decrypt(tampered) is None


def test_file_round_trip():
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "sample.bin"
        source.write_bytes(b"hello" * 20000)
        encryptor = FileEncryption("test-password")
        encrypted, message = encryptor.encrypt_file(str(source))
        assert message == "Success"
        assert encrypted
        decrypted, message = encryptor.decrypt_file(encrypted)
        assert message == "Success"
        assert decrypted
        assert Path(decrypted).read_bytes() == source.read_bytes()


def test_file_wrong_password_fails_closed():
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "sample.bin"
        source.write_bytes(b"confidential" * 1024)
        encrypted, message = FileEncryption("correct-password").encrypt_file(str(source))
        assert message == "Success"
        decrypted, message = FileEncryption("wrong-password").decrypt_file(encrypted)
        assert decrypted is None
        assert message == "Invalid padding or wrong password"

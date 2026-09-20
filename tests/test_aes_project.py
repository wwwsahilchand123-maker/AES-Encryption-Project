from pathlib import Path
import tempfile

from aes_project import TextEncryption, FileEncryption


def test_text_round_trip():
    encryptor = TextEncryption("test-password")
    plaintext = "AES round-trip test"
    ciphertext = encryptor.encrypt(plaintext)
    assert ciphertext
    assert encryptor.decrypt(ciphertext) == plaintext


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

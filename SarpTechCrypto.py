from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def encrypt(content: str, generated_key: bytes) -> str:
    fernet = Fernet(generated_key)
    encrypted_content = fernet.encrypt(content.encode()).decode()
    return encrypted_content

def decrypt(content: str, generated_key: bytes) -> str:
    fernet = Fernet(generated_key)
    decrypted_content = fernet.decrypt(content).decode()
    return decrypted_content

def generate_key(key):
    salt = b"1234567890abcdef"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    generated_key = base64.urlsafe_b64encode(kdf.derive(key.encode()))

    return generated_key
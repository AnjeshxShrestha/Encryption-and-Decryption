from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

class AESCipher:
    def __init__(self, key):
        self.key = key[:32].ljust(32, b'\0')

    def encrypt(self, data):
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        return base64.b64encode(iv + ct_bytes).decode()

    def decrypt(self, enc):
        raw = base64.b64decode(enc)
        iv = raw[:16]
        ct = raw[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()

if __name__ == "__main__":
    key = input("Enter encryption key: ").encode()
    choice = input("Encrypt or Decrypt? (e/d): ").lower()
    aes = AESCipher(key)
    
    if choice == 'e':
        data = input("Enter data to encrypt: ")
        encrypted = aes.encrypt(data)
        print(f"Encrypted: {encrypted}")
    elif choice == 'd':
        data = input("Enter data to decrypt: ")
        try:
            decrypted = aes.decrypt(data)
            print(f"Decrypted: {decrypted}")
        except:
            print("Decryption failed. Invalid key or data.")

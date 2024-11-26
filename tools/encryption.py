from cryptography.fernet import Fernet

# Generate key (run this once and save it)
# key = Fernet.generate_key()
# print(key)

KEY = b'YOUR_GENERATED_KEY_HERE'

def encrypt(data):
    cipher = Fernet(KEY)
    return cipher.encrypt(data.encode()).decode()

def decrypt(data):
    cipher = Fernet(KEY)
    return cipher.decrypt(data.encode()).decode()

import os

from Crypto.Random import get_random_bytes

from utils import AES_GCM, PERSISTENT_HANDLE, TPM2

SECRETS_DIR = "secrets"

if __name__ == "__main__":
    if PERSISTENT_HANDLE not in TPM2.get_handles_persistent().decode():
        key = get_random_bytes(16)
        if TPM2.seal(key):
            print("AES key sealed successully!")
    else:
        print("AES key is already persisted!")

    for file_name in os.listdir(SECRETS_DIR):
        file_name = os.path.join(SECRETS_DIR, file_name)
        with open(file_name, "rb") as f:
            content = f.read()
        with open(file_name + ".enc", "wb") as f:
            f.write(AES_GCM.encrypt(content))
        os.remove(file_name)

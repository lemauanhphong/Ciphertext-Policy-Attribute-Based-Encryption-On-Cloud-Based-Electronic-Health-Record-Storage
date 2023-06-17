import subprocess
import sys
from traceback import print_exc

import jwt
from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from charm.core.engine.util import bytesToObject, objectToBytes
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup
from Crypto.Cipher import AES

from config import JWT_PRIVKEY

PERSISTENT_HANDLE = "0x81008742"


class ABE:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.pairing_group = PairingGroup("SS512")
        self.hyb_abe = HybridABEnc(CPabe_BSW07(self.pairing_group), self.pairing_group)

        with open("./secrets/abe_keys.txt.enc", "rb") as f:
            key_pair = AES_GCM.decrypt(f.read())
            if key_pair is None:
                sys.exit()

        self.public_key, self.master_key = key_pair.splitlines()
        self.public_key = bytesToObject(self.public_key, self.pairing_group)
        self.master_key = bytesToObject(self.master_key, self.pairing_group)

    def get_public_key(self):
        return objectToBytes(self.public_key, self.pairing_group)

    def get_master_key(self):
        return objectToBytes(self.master_key, self.pairing_group)

    def gen_secret_key(self, attributes: list):
        return objectToBytes(self.hyb_abe.keygen(self.public_key, self.master_key, attributes), self.pairing_group)


class AES_GCM:
    @classmethod
    def encrypt(cls, data: bytes):
        e = AES.new(TPM2.unseal(), AES.MODE_GCM)  # nonce
        try:
            cipher, tag = e.encrypt_and_digest(data)  # cipher, tag
            return e.nonce + cipher + tag
        except Exception:
            print_exc()
            print("Encryption failed")
            return None

    @classmethod
    def decrypt(cls, data: bytes):
        d = AES.new(TPM2.unseal(), AES.MODE_GCM, data[:16])  # nonce
        try:
            return d.decrypt_and_verify(data[16:-16], data[-16:])  # cipher, tag
        except Exception:
            print_exc()
            print("Decryption failed")
            return None


class TPM2:
    @classmethod
    def get_handles_persistent(cls):
        return subprocess.run(["tpm2_getcap", "handles-persistent"], capture_output=True).stdout

    @classmethod
    def seal(cls, secret):
        subprocess.run(["tpm2_createprimary", "-Q", "-C", "o", "-c", "prim.ctx"])
        subprocess.run(
            ["tpm2_create", "-Q", "-g", "sha256", "-u", "seal.pub", "-r", "seal.priv", "-i-", "-C", "prim.ctx"],
            input=secret,
        )
        subprocess.run(
            [
                "tpm2_load",
                "-Q",
                "-C",
                "prim.ctx",
                "-u",
                "seal.pub",
                "-r",
                "seal.priv",
                "-n",
                "seal.name",
                "-c",
                "seal.ctx",
            ]
        )
        p = subprocess.run(["tpm2_evictcontrol", "-C", "o", "-c", "seal.ctx", PERSISTENT_HANDLE], capture_output=True)
        return b"action: persisted" in p.stdout

    @classmethod
    def unseal(cls):
        return subprocess.run(["tpm2_unseal", "-Q", "-c", PERSISTENT_HANDLE], capture_output=True).stdout


def gen_token(data):
    return jwt.encode(data, JWT_PRIVKEY, algorithm="EdDSA")

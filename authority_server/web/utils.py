import subprocess

import jwt
from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from charm.core.engine.util import bytesToObject, objectToBytes
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup

from config import JWT_PRIVKEY, PERSISTENT_HANDLE


class ABE:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.pairing_group = PairingGroup("SS512")
        self.hyb_abe = HybridABEnc(CPabe_BSW07(self.pairing_group), self.pairing_group)

        with open("/run/secrets/abe_keys", "rb") as f:
            self.public_key, self.master_key = f.read().splitlines()

        self.public_key = bytesToObject(self.public_key, self.pairing_group)
        self.master_key = bytesToObject(self.master_key, self.pairing_group)

    def get_public_key(self):
        return objectToBytes(self.public_key, self.pairing_group)

    def get_master_key(self):
        return objectToBytes(self.master_key, self.pairing_group)

    def gen_secret_key(self, attributes: list):
        return objectToBytes(self.hyb_abe.keygen(self.public_key, self.master_key, attributes), self.pairing_group)


def gen_token(data):
    return jwt.encode(data, JWT_PRIVKEY, algorithm="EdDSA")


def get_handles_persistent():
    return subprocess.run(["tpm2_getcap", "handles-persistent"], capture_output=True).stdout


def seal_secret(secret):
    subprocess.run(["tpm2_createprimary", "-Q", "-C", "o", "-c", "prim.ctx"])
    subprocess.run(
        ["tpm2_create", "-Q", "-g", "sha256", "-u", "seal.pub", "-r", "seal.priv", "-i-", "-C", "prim.ctx"],
        input=secret,
    )
    subprocess.run(
        ["tpm2_load", "-Q", "-C", "prim.ctx", "-u", "seal.pub", "-r", "seal.priv", "-n", "seal.name", "-c", "seal.ctx"]
    )
    p = subprocess.run(["tpm2_evictcontrol", "-C", "o", "-c", "seal.ctx", PERSISTENT_HANDLE], capture_output=True)
    return b"action: persisted" in p.stdout


def unseal_secret():
    return subprocess.run(["tpm2_unseal", "-Q", "-c", PERSISTENT_HANDLE], capture_output=True).stdout


abe = ABE()

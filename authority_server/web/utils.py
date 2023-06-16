import jwt
from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from charm.core.engine.util import bytesToObject, objectToBytes
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup

from config import JWT_PRIVKEY


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


abe = ABE()

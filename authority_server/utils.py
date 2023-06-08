import jwt
from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from charm.core.engine.util import objectToBytes
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup
from config import JWT_PRIVKEY


class ABE:
    def __init__(self):
        self.pairing_group = PairingGroup("SS512")
        self.hyb_abe = HybridABEnc(CPabe_BSW07(self.pairing_group), self.pairing_group)
        self.public_key, self.master_key = self.hyb_abe.setup()

        with open(".keys", "wb") as f:
            f.write(self.get_public_key())
            f.write(b"\n")
            f.write(self.get_master_key())

    def get_public_key(self):
        return objectToBytes(self.public_key, self.pairing_group)

    def get_master_key(self):
        return objectToBytes(self.master_key, self.pairing_group)

    def gen_secret_key(self, attributes: list):
        return objectToBytes(self.hyb_abe.keygen(self.public_key, self.master_key, attributes), self.pairing_group)


def gen_token(data):
    return jwt.encode(data, JWT_PRIVKEY, algorithm="EdDSA")


abe = ABE()

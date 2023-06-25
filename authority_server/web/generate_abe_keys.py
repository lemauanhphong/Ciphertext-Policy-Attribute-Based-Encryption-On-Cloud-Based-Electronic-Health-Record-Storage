from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from charm.core.engine.util import objectToBytes
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup

pairing_group = PairingGroup("SS512")
hyb_abe = HybridABEnc(CPabe_BSW07(pairing_group), pairing_group)
public_key, master_key = hyb_abe.setup()

with open("./secrets/abe_keys.txt", "wb") as f:
    f.write(objectToBytes(public_key, pairing_group))
    f.write(b"\n")
    f.write(objectToBytes(master_key, pairing_group))

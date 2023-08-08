from typing import Optional
from typing import Dict
import ecdsa
from phe import paillier
from ecdsa import SECP256k1
from ecdsa.util import randrange, string_to_number
from flow_py_sdk.signer.hash_algo import HashAlgo
from flow_py_sdk.signer.in_memory_verifier import InMemoryVerifier
from flow_py_sdk.signer.sign_algo import SignAlgo
from flow_py_sdk.signer.signer import Signer
from flow_py_sdk.signer.verifier import Verifier
from ecdsa.numbertheory import inverse_mod


class InMemorySigner(Signer, Verifier):
    def __init__(
            self, *, hash_algo: HashAlgo, sign_algo: SignAlgo, private_key_hex: str, multi_sig: Dict = None,
            wallet: str = None,
    ) -> None:
        super().__init__()
        self.hash_algo = hash_algo
        self.key = ecdsa.SigningKey.from_string(
            bytes.fromhex(private_key_hex), curve=sign_algo.get_signing_curve()
        )
        self.private_key_hex = private_key_hex
        self.multi_sig = multi_sig
        self.wallet = wallet
        self.verifier = InMemoryVerifier(
            hash_algo=hash_algo,
            sign_algo=sign_algo,
            public_key_hex=self.key.get_verifying_key().to_string().hex(),
        )

    def sign(self, message: bytes, tag: Optional[bytes] = None) -> bytes:
        hash_ = self._hash_message(message, tag)
        return self.key.sign_digest_deterministic(hash_)

    def verify(self, signature: bytes, message: bytes, tag: bytes) -> bool:
        return self.verifier.verify(signature, message, tag)

    def _hash_message(self, message: bytes, tag: Optional[bytes] = None) -> bytes:
        m = self.hash_algo.create_hasher()
        if tag:
            m.update(tag + message)
        else:
            m.update(message)
        return m.digest()

    def multisign(self, message: bytes, tag: Optional[bytes] = None):
        hash_ = self._hash_message(message, tag)
        q = SECP256k1.generator.order()
        k2 = randrange(SECP256k1.generator.order()) % q
        R2 = (k2 * SECP256k1.generator).scale()
        x2 = int(self.private_key_hex, 16)
        R1_x = int(self.multi_sig['R1.x'][2:], 16)
        R1_y = int(self.multi_sig['R1.y'][2:], 16)
        R = ecdsa.ellipticcurve.PointJacobi(SECP256k1.curve, R1_x, R1_y, 1) * k2
        r = R.x()
        row = randrange(SECP256k1.generator.order() * 2)
        pk = paillier.PaillierPublicKey(int(self.multi_sig['pk'][2:], 16))
        c_key = paillier.EncryptedNumber(pk, int(self.multi_sig['c_key'][2:], 16))
        c1_plain = row * q + (inverse_mod(k2, q) * string_to_number(hash_) % q)
        v = (inverse_mod(k2, q) * r * x2) % q
        c1 = pk.encrypt(c1_plain)
        c2 = v * c_key
        c3 = c1 + c2
        signed_message = c3.ciphertext()
        res_multisig = {'sig': hex(signed_message), 'script': self.multi_sig['script'],
                        'R2.x': hex(R2.x()), 'R2.y': hex(R2.y()), 'wallet': self.wallet, 'hash': hash_.hex()}
        return res_multisig





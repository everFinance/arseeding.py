import hashlib
from arweave import deep_hash
from jose.utils import base64url_decode, base64url_encode
from .tags import serialize_tags

sig_conf = {
    'ar': {
        'signature_type': 1,
        'sig_length': 512,
        'pub_length': 512,
        'sig_name': 'arweave'
    }
}

class BundleItem:
    def __init__(self, signer, target, anchor, tags, data):
        self.signer = signer
        self.signature_type = sig_conf[signer.type.lower()]['signature_type']
        self.owner = signer.owner
        self.target = target
        self.anchor = anchor
        self.tags = tags
        self.data = data
        self.sign()
        self.binary = self.get_item_binary()
    
    def get_data_to_sign(self):
        datalist = [
            b'dataitem',
            b'1',
            str(self.signature_type).encode(),
            base64url_decode(self.signer.owner.encode()),
            #self.target.encode(),
            #self.anchor.encode(),
            #serialize_tags(self.tags),
            b'',
            b'',
            b'',
            self.data
        ]
        return deep_hash.deep_hash(datalist)

    def sign(self):
        data = self.get_data_to_sign()
        if self.signer.type == 'AR':
            sig = self.signer.wallet.sign(data)
            self.id = base64url_encode(hashlib.sha256(sig).digest()).decode()
            self.signature = base64url_encode(sig).decode()

    def get_item_binary(self):
        if not self.id or not self.signature:
            raise ValueError("no signature")
        st = self.signature_type.to_bytes(2, byteorder='little')
        sig = base64url_decode(self.signature.encode())
        owner = base64url_decode(self.signer.owner.encode())
        data = self.data      
        return st+sig+owner+b"\x00\x00"+(0).to_bytes(8, byteorder='little') +(0).to_bytes(8, byteorder='little')+data
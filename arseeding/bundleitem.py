import hashlib
from eth_keys import keys
from arweave import deep_hash
from jose.utils import base64url_decode, base64url_encode
from .tags import serialize_tags

sig_conf = {
    'ar': {
        'signature_type': 1,
        'sig_length': 512,
        'pub_length': 512,
        'sig_name': 'arweave'
    },
    'eth': {
        'signature_type': 3,
        'sig_length': 65,
        'pub_length': 65,
        'sig_name': 'ethereum'
    },
}

class BundleItem:
    def __init__(self, signer, target, anchor, tags, data):
        self.signer = signer
        self.signature_type = sig_conf[signer.type.lower()]['signature_type']
        
        if self.signature_type == 1:
            self.owner = signer.owner
        elif self.signature_type == 3:
            self.owner = base64url_encode(b'\x04'+keys.PrivateKey(bytes.fromhex(signer.private_key)).public_key.to_bytes()).decode()
        else:
            raise('signer have not support')

        self.target = ''
        if target:
            if len(base64url_decode(target.encode())) != 32:
                raise ValueError('length of target is 32')
            self.target = target
        
        self.anchor = ''
        if anchor:
            # /tx_anchor return anchor is 48 byte.
            if len(base64url_decode(anchor.encode())) != 32:
                raise ValueError('length of anchor is 32')
            self.anchor = anchor

        self.tags = tags
        self.data = data
        self.sign()
        self.binary = self.get_item_binary()
    
    def get_data_to_sign(self):
        tags = b''
        if self.tags:
            tags = serialize_tags(self.tags)
        
        datalist = [
            b'dataitem',
            b'1',
            str(self.signature_type).encode(),
            base64url_decode(self.owner.encode()),
            base64url_decode(self.target.encode()),
            base64url_decode(self.anchor.encode()),
            tags,
            self.data
        ]
        return deep_hash.deep_hash(datalist)

    def sign(self):
        data = self.get_data_to_sign()
        if self.signature_type == 1:
            sig = self.signer.wallet.sign(data)
            
        elif self.signature_type == 3:
            sig = self.signer.sign(data)
            sig = bytes.fromhex(sig[2:])
        else:
            raise('signer have not support')
    
        self.id = base64url_encode(hashlib.sha256(sig).digest()).decode()
        self.signature = base64url_encode(sig).decode()

    def get_item_binary(self):
        if not self.id or not self.signature:
            raise ValueError("no signature")
        st = self.signature_type.to_bytes(2, byteorder='little')
        sig = base64url_decode(self.signature.encode())
        owner = base64url_decode(self.owner.encode())
        
        if self.target:
            target = base64url_decode(self.target.encode())
        if self.anchor:
            anchor = base64url_decode(self.anchor.encode())

        data = self.data      

        binary = st + sig + owner
        
        if self.target:
            binary += b'\x01' + target
        else:
            binary += b'\x00'
        
        if self.anchor:
            binary += b'\x01' + anchor
        else:
            binary += b'\x00'
        
        if self.tags:
            tags = serialize_tags(self.tags)
            binary += (len(self.tags)).to_bytes(8, byteorder='little')
            binary += (len(tags)).to_bytes(8, byteorder='little')
            binary += tags
        else:
            binary += (0).to_bytes(8, byteorder='little') + (0).to_bytes(8, byteorder='little')

        binary += data
        return binary
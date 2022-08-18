import os, json, mimetypes
from optparse import OptionParser  
import arseeding, everpay
# ar account

parser = OptionParser()  
parser.add_option("-d", "--dir", dest="dir",  
                  help="directory to upload to arweave")
parser.add_option("-w", "--wallet",  dest="wallet", 
                  help="eth/ar wallet file")
parser.add_option("-t", "--token",  dest="token", default="usdc",
                  help="token to pay")
parser.add_option("-i", "--index",  dest="index", default="index.html",
                  help="token to pay")
  
(options, args) = parser.parse_args()  

def get_singer(fn):
    try:
        json.load(open(fn))
    except json.JSONDecodeError:
        return everpay.ETHSigner(open(fn).reade().strip())
    else:
        return everpay.ARSigner(fn)

signer = get_singer(options.wallet)
manifest = {}
for root, dirs, files in os.walk(options.dir):
    for name in files:
        fn = os.path.join(root, name)
        data = open(fn, 'rb').read()

        tags = []
        if mimetypes.guess_type(name)[0]:
            tags = [
                {'name':'Content-Type', 'value':mimetypes.guess_type(name)[0]},
            ]

        order = arseeding.send_and_pay(signer, options.token, data, tags=tags)
        path = '/'.join(os.path.join(root, name).split('/')[1:])
        manifest[path] = order
        print(f'uploaded {name}', path, order['itemId'], order['fee'], '\n')

manifest_file = {
  "manifest": "arweave/paths",
  "version": "0.1.0",
  "index": {
    "path": options.index
  }
}

paths = {}
total = 0
for path, order in manifest.items():
    total += int(order['fee'])
    paths[path] = {"id": order['itemId']}
manifest_file["paths"] = paths

manifest_file_json = json.dumps(manifest_file)
print(manifest_file_json, '\n')
tags = [
    {'name':'Content-Type', 'value':'application/x.arweave-manifest+json'},
]
order = arseeding.send_and_pay(signer, options.token, manifest_file_json.encode(), tags=tags)
print(order['itemId'], order['fee'])
total += int(order['fee'])
print(total)
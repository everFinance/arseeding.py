# everpay.py

Python sdk for [arseeding](https://github.com/everFinance/arseeding).

Install with

```
pip install arseeding
```


## Quick start

upload file python.pdf and folder public to arweave using arseeding, and pay with usdc in your everapy account.

```python

import arseeding, everpay
# ar account
#signer = everpay.ARSigner('ar_wallet.json')
# eth account 
signer = everpay.ETHSigner(pk)
data = open('python.pdf', 'rb').read()
o = arseeding.send_and_pay(signer, 'usdc', data)
print(o['itemId'])

#file id is o['itemId'], you could get you file in url https://arseed.web3infura.io/o['itemId'] or http://arweave.net/o['itemId'] in a few minutes

# upload folder public
arseeding.upload_folder_and_pay(signer, 'usdc', 'public', slient=False)
```

## Command Line Tool: arseed

arseeding.py package have an Command Line Tool **arseed**


![image](/assets/arseed.gif)

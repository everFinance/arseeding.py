# everpay.py

Python sdk for [arseeding] (https://github.com/everFinance/arseeding).

Install with

```
pip install arseeding
```


- Quick start

upload python.pdf to arweave using arseeding

```python

import arseeding, everpay
# ar account
signer = everpay.ARSigner('ar_wallet.json')
data = open('game.py', 'rb').read()
o = arseeding.send_and_pay(signer, 'usdc', data)
print(o)

```
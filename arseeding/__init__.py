import requests, json
import everpay
from .bundleitem import BundleItem

arseed_url = 'https://arseed.web3infura.io'
pay_url = 'https://api.everpay.io'
def send_and_pay(signer, currency, data, target='', anchor='', tags=[], arseed_url=arseed_url):
    if data == type(''):
        data = data.encode()
    
    b = BundleItem(signer, target, anchor, tags, data)
    url = "%s/bundle/tx/%s"%(arseed_url, currency)
    res = requests.post(url=url,
                    data=b.binary,
                    headers={'Content-Type': 'application/octet-stream'}
    )
   
    if res.status_code == 200:
        order = res.json()
        
        account = everpay.Account(pay_url, signer)
        account.transfer(currency, order['bundler'], int(order['fee']), data=json.dumps(order))

        return order    


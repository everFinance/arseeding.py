import requests, json
import everpay
from .bundleitem import BundleItem

arseed_url = 'https://arseed.web3infra.dev'
pay_url = 'https://api.everpay.io'

def send_and_pay(signer, currency, data, target='', anchor='', tags=[], arseed_url=arseed_url, pay_url=pay_url):
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
        if pay_url:
            data = {"appName":"arseeding","action":"payment","itemIds":[order['itemId']]}
            account = everpay.Account(pay_url, signer)
            account.transfer(currency, order['bundler'], int(order['fee']), data=json.dumps(data))

        return order

def pay(signer, currency, fee, bundler_addr, item_ids, pay_url=pay_url):
    data = {"appName":"arseeding","action":"payment","itemIds":item_ids}
    account = everpay.Account(pay_url, signer)
    return account.transfer(currency, bundler_addr, int(fee), data=json.dumps(data))
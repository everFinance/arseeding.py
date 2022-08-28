import requests, json, os, mimetypes
from colorama import Fore, Style
import everpay
from .bundleitem import BundleItem

arseeding_url = 'https://arseed.web3infra.dev'
pay_url = 'https://api.everpay.io'

def send_and_pay(signer, currency, data, target='', anchor='', tags=[], arseeding_url=arseeding_url, pay_url=pay_url):
    if data == type(''):
        data = data.encode()
    
    b = BundleItem(signer, target, anchor, tags, data)
    url = "%s/bundle/tx/%s"%(arseeding_url, currency)
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

def pay(signer, currency, fee, to, item_ids, pay_url=pay_url):
    data = {"appName":"arseeding","action":"payment","itemIds":item_ids}
    account = everpay.Account(pay_url, signer)
    return account.transfer(currency, to, int(fee), data=json.dumps(data))

def upload_folder_and_pay(signer, currency, folder, index_page='index.html', arseeding_url=arseeding_url, pay_url=pay_url, silent=True):
    if not silent:
        print(f'Start to upload folder: {folder} \n')
    manifest = {}
    for root, dirs, files in os.walk(folder):
        for name in files:
            fn = os.path.join(root, name)
            data = open(fn, 'rb').read()

            tags = []
            if mimetypes.guess_type(name)[0]:
                tags = [
                    {'name':'Content-Type', 'value':mimetypes.guess_type(name)[0]},
                ]

            order = send_and_pay(signer, currency, data, tags=tags, arseeding_url=arseeding_url, pay_url='')
            path = '/'.join(os.path.join(root, name).split('/')[1:])
            manifest[path] = order
            if not silent:
                print(f'{Fore.GREEN}✓{Style.RESET_ALL} Upload {name}', path, order['itemId'], order['fee'])
    print()
    manifest_file = {
    "manifest": "arweave/paths",
    "version": "0.1.0",
    "index": {
        "path": index_page
    }
    }

    paths = {}
    total_fee = 0
    item_ids = []
    n = 0
    for path, order in manifest.items():
        total_fee += int(order['fee'])
        paths[path] = {"id": order['itemId']}
        item_ids.append(order['itemId'])
        n += 1
    to = order['bundler']
    pay(signer, currency, total_fee, to, item_ids, pay_url=pay_url)
    
    manifest_file["paths"] = paths
    manifest_file_json = json.dumps(manifest_file)
    tags = [
        {'name':'Content-Type', 'value':'application/x.arweave-manifest+json'},
    ]
    order = send_and_pay(signer, currency, manifest_file_json.encode(), tags=tags, arseeding_url=arseeding_url, pay_url=pay_url)
    total_fee += int(order['fee'])
    item_id = order['itemId']
    total_fee2 = total_fee/10**int(order['decimals'])
    
    if not silent:
        print(f'{Fore.GREEN}✓{Style.RESET_ALL} Uploaded folder {folder}. File number: {n+1}; Total Fee: {Fore.GREEN}{total_fee2} {currency.upper()}{Style.RESET_ALL}; URL: {Fore.BLUE}{arseeding_url}/{item_id}{Style.RESET_ALL}')
    
    return order['itemId'], total_fee, total_fee2
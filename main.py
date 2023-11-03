import codecs, json, requests, binascii
from settings import REST_HOST, MACAROON_PATH, TLS_PATH

def mint(macaroon, metadata):
    url = f'https://{REST_HOST}/v1/taproot-assets/assets'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    asset_metadata = bytes(metadata, 'utf-8')
    asset_metadata = binascii.hexlify(asset_metadata)
    asset_metadata = asset_metadata.decode('utf-8')
    data = {
        'asset': {
            'asset_type': 0,
            'name': 'REST Mint',
            'asset_meta': {
                'data': asset_metadata,
                'type': 0,
            },
            'amount': 1000
        },
        'enable_emission': False,
        'short_response': False,
    }
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=TLS_PATH)
    return r

def list_batch(macaroon, batch_key):
    url = f'https://{REST_HOST}/v1/taproot-assets/assets/mint/batches/{batch_key}'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    r = requests.get(url, headers=headers, verify=TLS_PATH)
    print(r.json())

def finalize_batch(macaroon):
    url = f'https://{REST_HOST}/v1/taproot-assets/assets/mint/finalize'
    headers = {'Grpc-Metadata-macaroon': macaroon}
    data = {
    'short_response': True,
    }
    r = requests.post(url, headers=headers, data=json.dumps(data), verify=TLS_PATH)
    print(r.json())

def main():
    macaroon = codecs.encode(open(MACAROON_PATH, 'rb').read(), 'hex')
    response = mint(macaroon, 'Testing metadata')
    print(response)

if __name__ == '__main__':
    main()

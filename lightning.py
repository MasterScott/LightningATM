import os, codecs, requests, json
from config import *


def payout(amt, payment_request):
    with open(os.path.expanduser('~/admin.macaroon'), 'rb') as f:
        macaroon_bytes = f.read()
        macaroon = codecs.encode(macaroon_bytes, 'hex')

    data = {
            'payment_request': payment_request,
            'amt': round(amt),
    }

    response =  requests.post(
        str(APIURL) + '/channels/transactions',
        headers = {'Grpc-Metadata-macaroon': macaroon},
        data=json.dumps(data),
    )

def lastpayment(payment_request):
    with open(os.path.expanduser('~/admin.macaroon'), 'rb') as f:
        macaroon_bytes = f.read()
        macaroon = codecs.encode(macaroon_bytes, 'hex')

    url = str(APIURL) + '/payments'

    data = {
            'include_incomplete': True,
    }

    r = requests.get(url, headers = {'Grpc-Metadata-macaroon': macaroon}, data=json.dumps(data))
    json_data = json.loads(r.text)
    payment_data = json_data['payments']
    last_payment = payment_data[-1]

    if (last_payment['payment_request'] == payment_request) and (last_payment['status'] == 'SUCCEEDED'):
        return 'Success'
    else:
        return 'Payment failed'

def decoderequest(payment_request):
    if payment_request:
        with open(os.path.expanduser('~/admin.macaroon'), 'rb') as f:
            macaroon_bytes = f.read()
            macaroon = codecs.encode(macaroon_bytes, 'hex')

        url = str(APIURL) + '/payreq/' + str(payment_request)

        r = requests.get(url, headers = {'Grpc-Metadata-macaroon': macaroon})
        json_data = json.loads(r.text)
        request_data = json_data

        if 'lnbc1p' in payment_request:
            print('Zero sat invoice')
            return True
        else:
            return request_data['num_satoshis']
    else:
        pass

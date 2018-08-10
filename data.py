import os
import requests

CHAIN_RIDER_TOKEN = os.environ['CHAIN_RIDER_TOKEN']

class ChainRider:

    base_url = 'https://api.chainrider.io/v1'

    def __init__(self, currency='dash', blockchain='main'):
        self.currency = currency
        self.chain = blockchain
        self.token = CHAIN_RIDER_TOKEN

    def block(self, header):
        r = requests.get(os.path.join(self.base_url,
                                      self.currency,
                                      self.chain,
                                      'block',
                                      header + '?' + 'token=' + self.token))

        return r.json()

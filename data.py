from datetime import datetime
from datetime import timedelta
import os
import pickle
import requests
import sys
import time

CHAIN_RIDER_TOKEN = os.environ['CHAIN_RIDER_TOKEN']
DATA_DIR = os.environ['ORDER_DATA_PATH']

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

    def block_hash(self, index):
        r = requests.get(os.path.join(self.base_url,
                                      self.currency,
                                      self.chain,
                                      'blockindex',
                                      repr(index) + '?' + 'token=' + self.token))

        return r.json()['blockHash']

    def block_date(self, date):
        params = 'token=' + self.token
        params += '&limit=' + repr(sys.maxsize)
        params += '&blockDate=' + date

        r = requests.get(os.path.join(self.base_url,
                                      self.currency,
                                      self.chain,
                                      'blocks?' + params))

        return r.json()

    def block_txs(self, header, page=0):
        params = 'block=' + header
        params += '&pageNum=' + repr(page)
        params += '&token=' + self.token

        r = requests.get(os.path.join(self.base_url,
                                      self.currency,
                                      self.chain,
                                      'txs?' + params))

        if r.status_code != 200:
            raise RuntimeError('error %d: %s' % (r.status_code, r.text))

        result = r.json()
        txs = result['txs']

        if page < result['pagesTotal']-1:
            return txs + self.block_txs(header, page+1)    

        return txs

def download_txs(begin_stamp, end_stamp=datetime.now().strftime('%Y-%m-%d')):
    cur_date = datetime.strptime(begin_stamp, '%Y-%m-%d')
    end_date = datetime.strptime(end_stamp, '%Y-%m-%d')
    day = timedelta(hours=24)

    rider = ChainRider()
    tx_map = {}
    while cur_date <= end_date:
        blocks = rider.block_date(cur_date.strftime('%Y-%m-%d'))['blocks']
        block_hashes = [blk['hash'] for blk in blocks]

        for block_hash in block_hashes:
            tx_map[block_hash] = rider.block_txs(block_hash)
            time.sleep(60)

        cur_date += day

    return tx_map

def dump_txs(tx_map, filename=os.path.join(DATA_DIR, 'dash_txs.dat')):
    with open(filename, 'wb') as fd:
        pickle.dump(tx_map, fd)

def load_txs(filename=os.path.join(DATA_DIR, 'dash_txs.dat')):
    with open(filename, 'rb') as fd:
        return pickle.load(fd)

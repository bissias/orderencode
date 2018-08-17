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

        status = None
        request_ct = 0
        while status != 200:
            try:
                r = requests.get(os.path.join(self.base_url,
                                              self.currency,
                                              self.chain,
                                              'txs?' + params))
                status = r.status_code
            except Exception as e:
                print('caught exception: %s' % str(e))
                status = None

            request_ct += 1

            if r.status_code != 200:
                print('error %d: %s' % (r.status_code, r.text))

                if request_ct > 3:
                    print('aborting')
                    break
                else:
                    print('retrying')
                    time.sleep(30)

        if status != 200:
            raise RuntimeError('download failed after 3 attempts')

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
        print('Downloading txs for %s' % cur_date.strftime('%Y-%m-%d %H:%M:%S'))
        blocks = rider.block_date(cur_date.strftime('%Y-%m-%d'))['blocks']
        blocks = sorted(blocks, key=lambda block: block['time'])
        block_hashes = [(blk['time'], blk['hash']) for blk in blocks]

        for block_time, block_hash in block_hashes:
            tx_map[(block_time, block_hash)] = rider.block_txs(block_hash)
            time.sleep(0.25)

        cur_date += day

    return tx_map

def dump_txs(tx_map, filename=os.path.join(DATA_DIR, 'dash_txs.dat')):
    with open(filename, 'wb') as fd:
        pickle.dump(tx_map, fd)

def load_txs(filename=os.path.join(DATA_DIR, 'dash_txs.dat')):
    with open(filename, 'rb') as fd:
        return pickle.load(fd)

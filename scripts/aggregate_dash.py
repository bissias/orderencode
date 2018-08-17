import data
from datetime import datetime
from datetime import timedelta
import os

DATA_DIR = os.environ['ORDER_DATA_PATH']

cur_date = datetime(year=2018, month=7, day=1)
end_date = datetime(year=2018, month=7, day=31)
day = timedelta(hours=24)

tx_map = {}
while cur_date <= end_date:
    cur_timestamp = cur_date.strftime('%Y-%m-%d')
    tx_map.update(data.load_txs(os.path.join(DATA_DIR, 'dash_txs_%s.dat' % cur_timestamp)))
    cur_date += day

data.dump_txs(tx_map)

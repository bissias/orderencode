import data

txs = data.download_txs('2018-08-01', '2018-08-01')
data.dump_txs(txs)
loaded_txs = data.load_txs()

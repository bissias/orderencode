import data

txs = data.download_txs('2018-07-15', '2018-07-15')
data.dump_txs(txs)
loaded_txs = data.load_txs()

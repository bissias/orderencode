import data

txs = data.download_txs('2018-07-15', '2018-07-15')
data.dump_txs(txs)
loaded_tx_map = data.load_txs()

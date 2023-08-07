from multiprocessing import Pool
from multiprocessing import Queue
from .chain_interface import ChainInterfaceDriver


class ChainInterfaceRaceDriver(ChainInterfaceDriver):

    def __init__(self, store, chain_interface, offset=0, target=-1, pre_callback=None, post_callback=None, block_callback=None, idle_callback=None, worker_count=0):
        super(ChainInterfaceRaceDriver, self).__init__(store, chain_interface, offset=offset, target=target, pre_callback=pre_callback, post_callback=post_callback, block_callback=block_callback, idle_callback=idle_callback)
        if worker_count > 0:
            self.workers = Pool(worker_count)
        else:
            self.workers = Pool()

        self.collector = Queue(1000)


    def fetch_remote(self, conn, item, block, tx_hash, tx=None):
        if tx == None:
            o = self.chain_interface.tx_by_hash(tx_hash, block=block)
            r = conn.do(o)
            tx = Tx.from_src(r)

        rcpt = conn.do(self.chain_interface.tx_receipt(tx.hash))
        if rcpt != None:
            tx.apply_receipt(self.chain_interface.src_normalize(rcpt))
        
        self.collector.put((tx, block,))

    
    def process(self, conn, item, block):
        i = item.tx_cursor
        handles = []
        while True:
            tx = None
            tx_hash = None
            # handle block objects regardless of whether the tx data is embedded or not
            try:
                tx = block.tx(i)
                tx_hash = tx.hash
            except AttributeError:
                tx_hash = block.txs[i]
            r = self.workers.apply_async(self.fetch_remote, (conn, item, block, tx_hash, tx,))
            handles.append(r)

            i += 1

        for h in handles:
            v = h.get()
            self.process_single(conn, v[0], v[1])


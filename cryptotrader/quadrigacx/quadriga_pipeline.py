'''
Loads data from QuadrigaCX.

@author: Tobias Carryer
'''

import json
import time
from threading import Thread
import urllib2

class QuadrigaPipeline(object):
    def __init__(self, on_order_book, product, poll_time=15):
        '''
        on_order_book should have 2 parameters: one for the bids and one for the asks.
        on_order_book will be called every [poll_time] seconds
        
        minutes_to_reset is used to force a disconnect and reconnect to the websocket
        every so many minutes.
        
        Pre: product is not a list
             minutes_to_reset is positive
             poll_time is a positive integer
        '''
        
        print("Created QuadrigaCX pipeline. Uses QuadrigaCX's websocket API.")
        
        self.on_order_book = on_order_book
        self.order_book_url = "https://api.quadrigacx.com/v2/order_book?book=" + product
        self.poll_time = poll_time
        self._time_started = 0
        
        self.stop = False
        self.thread = None

    def start(self):
        
        def _go():
            last_time = 0
            while True:
                if self.stop:
                    print "Stopping QuadrigaCX pipeline."
                    break
                elif time.time() - last_time >= self.poll_time:
                    last_time = time.time()
                    order_book = self.get_order_book()
                    self.on_order_book(order_book["bids"], order_book["asks"])

        self.thread = Thread(target=_go)
        self.stop = False
        self.thread.start()

    def get_order_book(self):
        '''
        Pre: self.order_book_url is valid
        Returns: JSON Dictionary with the entries "timestamp", "bids", and "asks"
                 The bids and asks are two 2D lists. Each entry has exactly two entries in its second level,
                 index 0 is the  order's price, and index 1 is the order's amount.
        '''
        
        # Imitate a browser.
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8'}

        req = urllib2.Request(self.order_book_url, headers=hdr)
        data = json.loads(urllib2.urlopen(req).read())
        return data

    def close(self):
        if not self.stop:
            self.stop = True

if __name__ == "__main__":

    def on_order_book(bids, asks):
        print("on_order_book was called.")
        print("Highest bid: "+bids[0][0]+"CAD for "+bids[0][1]+"ETH.")
        print("Lowest ask: "+asks[0][0]+"CAD for "+asks[0][1]+"ETH.")
        
    pipeline = QuadrigaPipeline(on_order_book, "eth_cad", 15)
    pipeline.start()
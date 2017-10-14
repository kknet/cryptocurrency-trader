'''
Makes buying and selling decisions.

@author: Tobias Carryer
'''

from abc import ABCMeta, abstractmethod

class Trader(object):
    
    __metaclass__ = ABCMeta
    
    def __init__(self, is_test, minimum_trade):
        print("Created a trader.")
        self.balance = None
        self.assets = None
        self.can_buy = True
        self.can_sell = True
        self.is_test = is_test
        self.minimum_trade = minimum_trade
    
    @abstractmethod
    def buy(self, market_value):
        '''
        Post: get_balance() is lower by percent_to_spend
        '''
        
        print("buy is expected to be overriden by a child of Trader")
        
    @abstractmethod
    def sell(self, market_value):
        '''
        Post: get_assets() is lower by percent_to_sell
        '''
        
        print("sell is expected to be overriden by a child of Trader")
        
    def hold(self, market_value):
        print("Need to override function 'hold' before using it")
        
    def abort(self):
        ''' Post: Trader will not buy or sell. '''
        self.can_buy = False
        self.can_sell = False
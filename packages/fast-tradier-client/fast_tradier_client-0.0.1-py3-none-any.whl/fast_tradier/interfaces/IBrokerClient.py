from interface import implements, Interface
from typing import Tuple, List, Dict, Optional

from fast_tradier.models.OptionOrder import OptionOrder
from fast_tradier.models.market_data.Quote import Quote
from fast_tradier.models.account.Position import Position
from fast_tradier.models.account.AccountBalance import AccountBalance

class IBrokerClient(Interface):

    def is_market_in_session_now(self) -> Tuple:
        raise NotImplementedError('not implemented in interface')
    
    def is_market_open_today(self, market: str='NYSE') -> Tuple:
        raise NotImplementedError('not implemented in interface')

    def get_quotes(self, symbols: List[str]):# -> List[Dict]:
        raise NotImplementedError('not implemented in interface')

    def get_order_status(self, order_id: int) -> str:
        raise NotImplementedError('not implemented in interface')

    def get_option_expirations(self, symbol: str) -> List[str]:
        raise NotImplementedError('not implemented in interface')
    
    def place_option_order(self, order: OptionOrder) -> Optional[int]:
        raise NotImplementedError('not implemented in interface') # returns order id
    
    def cancel_order(self, order_id: int) -> bool:
        raise NotImplementedError('not implemented in interface')
    
    def get_option_chain(self, symbol: str, expiration: str, greeks: bool = True) -> Optional[Dict]:
        raise NotImplementedError('not implemented in interface')

    def modify_option_order(self, modified_order: OptionOrder) -> bool:
        raise NotImplementedError('not implemented in interface')

    def get_positions(self) -> List[Position]:
        raise NotImplementedError('not implemented in interface')

    def get_account_balance(self) -> Optional[AccountBalance]:
        raise NotImplementedError('not implemented in interface')
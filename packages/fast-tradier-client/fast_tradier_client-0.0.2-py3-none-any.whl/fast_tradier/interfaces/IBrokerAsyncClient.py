from interface import Interface
from typing import Tuple, List, Dict, Optional

from fast_tradier.models.OptionOrder import OptionOrder
from fast_tradier.models.market_data.Quote import Quote
from fast_tradier.models.account.Position import Position
from fast_tradier.models.account.AccountBalance import AccountBalance

class IBrokerAsyncClient(Interface):

    async def is_market_in_session_now_async(self) -> Tuple:
        raise NotImplementedError('not implemented in interface')
    
    async def is_market_open_today_async(self, market: str='NYSE') -> Tuple:
        raise NotImplementedError('not implemented in interface')

    async def get_quotes_async(self, symbols: List[str]) -> List[Quote]:
        raise NotImplementedError('not implemented in interface')
    
    async def get_order_status_async(self, order_id: int) -> str:
        raise NotImplementedError('not implemented in interface')
    
    async def get_option_expirations_async(self, symbol: str) -> List[str]:
        raise NotImplementedError('not implemented in interface')
    
    async def place_option_order_async(self, order: OptionOrder) -> Optional[int]:
        raise NotImplementedError('not implemented in interface') # returns order id
    
    async def cancel_order_async(self, order_id: int) -> bool:
        raise NotImplementedError('not implemented in interface')

    async def get_option_chain_async(self, symbol: str, expiration: str, greeks: bool = True) -> Optional[Dict]:
        raise NotImplementedError('not implemented in interface')

    async def modify_option_order_async(self, modified_order: OptionOrder) -> bool:
        raise NotImplementedError('not implemented in interface')
    
    async def get_positions_async(self) -> List[Position]:
        raise NotImplementedError('not implemented in interface')
    
    async def get_account_balance_async(self) -> Optional[AccountBalance]:
        raise NotImplementedError('not implemented in interface')
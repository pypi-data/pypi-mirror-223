from interface import implements
from typing import Tuple, List, Dict, Optional
from datetime import datetime

import math
import arrow
import pandas as pd
import httpx
import json

from fast_tradier.interfaces.IBrokerClient import IBrokerClient
from fast_tradier.models.OptionOrder import OptionOrder
from fast_tradier.models.market_data.Quote import Quote
from fast_tradier.models.account.Position import Position
from fast_tradier.models.account.AccountBalance import AccountBalance
from fast_tradier.interfaces.IRealTimeQuoteProvider import IRealTimeQuoteProvider
from fast_tradier.utils.TimeUtils import US_Eastern_TZ, YYYYMDHHMM_Format, YMD_Format, YMDHMS_Format, TimeUtils
from fast_tradier.utils.OptionUtils import OptionChain_Headers

class FastTradierClient(implements(IBrokerClient)):
    '''tradier client for interacting with Tradier API'''

    def __init__(self, access_token: str, account_id: str, is_prod: bool = True, real_time_quote_provider: IRealTimeQuoteProvider = None):
        self.__bear_at = f'Bearer {access_token}'
        self.__auth_headers = {'Authorization': self.__bear_at, 'Accept': 'application/json'}
        self.__is_prod = is_prod
        self.__account_id = account_id
        self.__real_time_quote_provider = real_time_quote_provider
        self.__base_host = 'https://sandbox.tradier.com/v1/'
        if is_prod:
            self.__base_host = 'https://api.tradier.com/v1/'

    @property
    def market_open(self) -> datetime:
        return self.__market_open

    @property
    def market_close(self) -> datetime:
        return self.__market_close

    @property
    def index_close(self) -> datetime:
        return self.__index_close
    
    @property
    def host_base(self) -> str:
        return self.__base_host
    
    @property
    def account_id(self) -> str:
        return self.__account_id

    def today(self) -> datetime:
        return datetime.now(US_Eastern_TZ)

    def is_market_in_session_now(self) -> Tuple:
        is_open, day_arr_str, today_window = self.is_market_open_today()
        if not is_open:
            return False, False

        today = self.today()
        today_str = today.strftime(YMD_Format)
        open_hour = today_window['start']
        close_hour = today_window['end']
        index_close_hour = close_hour[: -2] + '15' # index options close at 16:15

        open_t = '{} {}'.format(today_str, open_hour) # make it look like '2022-01-22 09:30'
        close_t = '{} {}'.format(today_str, close_hour)
        index_close_t = '{} {}'.format(today_str, index_close_hour)
        self.__market_open = arrow.get(open_t, YYYYMDHHMM_Format, tzinfo=US_Eastern_TZ)
        self.__market_close = arrow.get(close_t, YYYYMDHHMM_Format, tzinfo=US_Eastern_TZ)
        self.__index_close = arrow.get(index_close_t, YYYYMDHHMM_Format, tzinfo=US_Eastern_TZ)
        is_index_open = (today <= self.index_close) #whether index options trade is still open

        if today < self.market_open or today > self.market_close:
            return False, is_index_open

        return True, True
    
    def is_market_open_today(self, market: str = 'NYSE') -> Tuple:
        today = self.today()
        url = 'https://api.tradier.com/v1/markets/calendar?month={}&year={}'.format(today.month, today.year)
        day_arr = []
        with httpx.Client() as client:
            response = client.get(url=url, headers=self.__auth_headers)
            json_res = response.json()
            day_arr_str = json.dumps(json_res["calendar"]["days"]["day"])
            day_arr = json.loads(day_arr_str)
        
        today_str = today.strftime("%Y-%m-%d")
        today_open_window = None

        is_open = False
        for day in day_arr:
            if day['date'] == today_str:
                if day['status'] == 'open':
                    is_open = True
                    today_open_window = day['open'] # {start: 09:30, end: 16:00}
                break

        return is_open, day_arr_str, today_open_window
    
    # https://documentation.tradier.com/brokerage-api/markets/get-quotes
    def get_quotes(self, symbols: List[str]) -> List[Quote]:
        '''get quote for symbol, could be stock or option symbol'''
        url = f'{self.host_base}markets/quotes'
        params = {'symbols': ','.join(symbols), 'greeks': 'false'}
        results = []
        with httpx.Client() as client:
            response = client.post(url=url, data=params, headers=self.__auth_headers)
            json_res = response.json()
            if 'quotes' in json_res and json_res['quotes'] is not None:
                quote_objs = json_res['quotes']['quote']

                if quote_objs is not None:
                    if isinstance(quote_objs, List):
                        '''API returns a list of quotes if input is a list of tickers'''
                        for quote_obj in quote_objs:
                            results.append(Quote(quote_obj))
                    elif isinstance(quote_objs, Dict):
                        '''API returns a single Dict object if input is a single ticker'''
                        results = [Quote(quote_objs)]

        return results

    def get_order_status(self, order_id: int) -> str:
        url = f'{self.host_base}user/orders'
        with httpx.Client() as client:
            response = client.get(url,
                                  params={},
                                  headers=self.__auth_headers)
            json_res = response.json()
            '''
            {'accounts': {'account': {'account_number': 'VA7xxxa231', 'orders': {'order': {'id': 6227976, 'type': 'market', 'symbol': 'SPX', 'side': 'buy', 'quantity': 2.0, 'status': 'pending', 'duration': 'day', 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 2.0, 'create_date': '2023-05-02T05:36:05.285Z', 'transaction_date': '2023-05-02T05:36:05.599Z', 'class': 'multileg', 'num_legs': 2, 'strategy': 'spread', 'leg': [{'id': 6227977, 'type': 'market', 'symbol': 'SPX', 'side': 'sell_to_open', 'quantity': 1.0, 'status': 'pending', 'duration': 'day', 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 1.0, 'create_date': '2023-05-02T05:36:05.285Z', 'transaction_date': '2023-05-02T05:36:05.599Z', 'class': 'option', 'option_symbol': 'SPXW230508C01800000'}, {'id': 6227978, 'type': 'market', 'symbol': 'SPX', 'side': 'buy_to_open', 'quantity': 1.0, 'status': 'pending', 'duration': 'day', 'avg_fill_price': 0.0, 'exec_quantity': 0.0, 'last_fill_price': 0.0, 'last_fill_quantity': 0.0, 'remaining_quantity': 1.0, 'create_date': '2023-05-02T05:36:05.285Z', 'transaction_date': '2023-05-02T05:36:05.599Z', 'class': 'option', 'option_symbol': 'SPXW230508C04800000'}]}}}}}
            '''
            # print('json_res: ', json_res)
            if 'accounts' in json_res:
                order_obj = json_res['accounts']['account']['orders']['order']
                if isinstance(order_obj, Dict):
                    if 'id' in order_obj and order_obj['id'] == order_id:
                        return order_obj['status']
                elif isinstance(order_obj, List):
                    for order in order_obj:
                        if 'id' in order and order['id'] == order_id:
                            return order['status']

        return None
    
    def get_option_expirations(self, symbol: str) -> List[str]:
        symbol = symbol.upper()
        url = f'{self.host_base}markets/options/expirations'
        with httpx.Client() as client:
            response = client.get(url, params={'symbol': symbol, 'includeAllRoots': 'true', 'strikes': 'false'}, headers=self.__auth_headers)
            json_res = response.json()
            print('json_res: ', json_res)
            if json_res["expirations"] is not None:
                return json_res["expirations"]["date"]

        return None
    
    def place_option_order(self, order: OptionOrder) -> Optional[int]:
        url = f'{self.host_base}accounts/{self.account_id}/orders'
        try:
            with httpx.Client() as client:
                response = client.post(url, data=order.to_json(), headers=self.__auth_headers)
                res = response.json()
                if 'order' in res and res['order']['status'].upper() == 'OK':
                    return res['order']['id']
        except Exception as ex:
            print('exception in place_option_order: ', ex)
            raise ex
    
    def cancel_order(self, order_id: int) -> bool:
        url = f'{self.host_base}accounts/{self.account_id}/orders/{order_id}'
        try:
            with httpx.Client() as client:
                response = client.delete(url=url, headers=self.__auth_headers)
                res = response.json()
                if 'order' in res and 'status' in res['order']:
                    return res['order']['status'].upper() == 'OK'
        except Exception as ex:
            print('exception in cancel_order: ', ex)

        return False

    def get_option_chain(self, symbol: str, expiration: str, greeks: bool = True) -> Optional[Dict]:
        url = f'{self.host_base}markets/options/chains'
        symbol = symbol.upper()

        try:
            call_options = []
            put_options = []

            with httpx.Client() as client:
                symbol_quotes = self.get_quotes([symbol])
                response = client.get(url, params={'symbol': symbol, 'expiration': expiration, 'greeks': greeks}, headers=self.__auth_headers)
                json_res = response.json()
                if json_res["options"] is not None:
                    chain = json_res["options"]["option"]
                    underlying_price = None
                    if self.__real_time_quote_provider is not None:
                        try:
                            underlying_price = self.__real_time_quote_provider.get_price(symbol)
                        except Exception as inner_ex:
                            print('exception getting real time quote: ', inner_ex)

                    if len(symbol_quotes) > 0 and underlying_price is None:
                        underlying_price = symbol_quotes[0].last

                    now_unixts = int(arrow.utcnow().datetime.timestamp())
                    for o in chain:
                        gamma = 0
                        delta = 0
                        vega = 0
                        greeks_nums = o['greeks']
                        if greeks_nums is not None: 
                            gamma = greeks_nums['gamma'] if greeks_nums['gamma'] is not None and not math.isnan(greeks_nums['gamma']) else 0
                            delta = greeks_nums['delta'] if greeks_nums['delta'] is not None and not math.isnan(greeks_nums['delta']) else 0
                            vega = greeks_nums['vega'] if greeks_nums['vega'] is not None and not math.isnan(greeks_nums['vega']) else 0

                        row = o['symbol'], o['strike'], 0 if pd.isna(o['last']) else o['last'], o['open_interest'], o['ask'], o['bid'], o['expiration_date'], TimeUtils.convert_unix_ts(o['bid_date']).strftime(YMDHMS_Format), o['volume'], underlying_price, now_unixts, gamma, delta, vega
                        if o['option_type'] == 'call':
                            call_options.append(row)
                        else:
                            put_options.append(row)

                call_df = pd.DataFrame(call_options)
                call_df.columns = OptionChain_Headers
                put_df = pd.DataFrame(put_options)
                put_df.columns = OptionChain_Headers
                return {
                    'expiration': expiration,
                    'ticker': symbol,
                    'call_chain': call_df,
                    'put_chain': put_df
                    }
        except Exception as ex:
            return None

    def modify_option_order(self, modified_order: OptionOrder) -> bool:
        url = f'{self.host_base}accounts/{self.account_id}/orders/{modified_order.id}'
        try:
            with httpx.Client() as client:
                response = client.put(url=url, data=modified_order.to_json(), headers=self.__auth_headers)
                res = response.json()
                if 'order' in res:
                    return res['order']['status'].upper() == 'OK'
                return False
        except Exception as ex:
            return False
    
    def get_positions(self) -> List[Position]:
        url = f'{self.host_base}accounts/{self.account_id}/positions'
        try:
            with httpx.Client() as client:
                response = client.get(url=url,
                                    params={},
                                    headers=self.__auth_headers)
                res = response.json()
                results = []
                if 'positions' in res:
                    for position_dict in res['positions']:
                        results.append(Position(position_dict))
                return results
        except Exception as ex:
            return []
    
    def get_account_balance(self) -> Optional[AccountBalance]:
        url = f'{self.host_base}accounts/{self.account_id}/balances'
        try:
            with httpx.Client() as client:
                response = client.get(url=url,
                                      params={},
                                      headers=self.__auth_headers)
                res = response.json()
                print('res: ', res)
                if 'balances' in res:
                    return AccountBalance(res['balances'])
        except Exception as ex:
            print('exception in get_account_balances: ', ex)

        return None
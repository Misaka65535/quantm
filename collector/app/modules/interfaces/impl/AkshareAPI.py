from ..query_interface_abstract_class import QueryInterfaceABC
import akshare as ak
import pandas as pd


class AkshareAPI(QueryInterfaceABC):

    def init(self, **kwargs):
        pass

    def after(self, **kwargs):
        pass

    def query_by_date(self, symbol: str, market_type: str, start_date: str, end_date: str, **kwargs) -> pd:
        match market_type:
            case ['sz', 'sh', '']:
                stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=symbol, period="daily",
                                                        start_date=start_date, end_date=end_date,
                                                        adjust="")
                return stock_zh_a_hist_df
            case _:
                pass

    def query_by_time_stamp(self, symbol: str, market_type: str, start_time: str, end_time: str, **kwargs) -> pd:
        pass

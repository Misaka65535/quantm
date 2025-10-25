from ..query_interface_abstract_class import QueryInterfaceABC
import baostock as bs
import pandas as pd


class BaoStockAPI(QueryInterfaceABC):
    def init(self):
        # 登陆系统
        lg = bs.login()
        # 显示登陆返回信息
        print('login respond error_code:' + lg.error_code)
        print('login respond  error_msg:' + lg.error_msg)
        pass

    def after(self, **kwargs):
        # 登出系统
        bs.logout()
        print('login out ')
        pass

    def query_by_date(self, symbol: str, market_type: str, start_date: str, end_date: str, **kwargs) -> pd:
        # 获取沪深A股历史K线数据
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        code = market_type + '.' + symbol
        rs = bs.query_history_k_data_plus(code,
                                          "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                          start_date=start_date, end_date=end_date,
                                          frequency="d", adjustflag="3")
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        return result

    def query_by_time_stamp(self, symbol: str, market_type: str, start_time: str, end_time: str, **kwargs) -> pd:
        pass

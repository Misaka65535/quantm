from abc import ABC
from abc import abstractmethod
import pandas as pd


class QueryInterfaceABC(ABC):
    """
    Query interface abstract class
    """

    @abstractmethod
    def init(self, **kwargs):
        """
        Initialize the interface
        :param kwargs: 自定义参数
        :return:
        """
        pass

    @abstractmethod
    def after(self, **kwargs):
        """
        After a query
        :param kwargs: 自定义参数
        :return:
        """
        pass

    @abstractmethod
    def query_by_date(self, symbol: str, market_type: str, start_date: str, end_date: str, **kwargs) -> pd:
        """
        Query data by date
        :param symbol: 代码
        :param market_type: 市场
        :param start_date: 查询起始日期
        :param end_date: 查询结束日期
        :param kwargs: 自定义参数
        :return: 查询结果
        """
        pass

    @abstractmethod
    def query_by_time_stamp(self, symbol: str, market_type: str, start_time: str, end_time: str, **kwargs) -> pd:
        """
        Query data by time stamp
        :param symbol: 代码
        :param market_type: 市场
        :param start_time: 查询起始时间
        :param end_time: 查询结束时间
        :param kwargs: 自定义参数
        :return: 查询结果
        """
        pass

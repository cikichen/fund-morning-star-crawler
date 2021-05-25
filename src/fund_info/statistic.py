'''
Desc: 基金统计
File: /statistic.py
Project: fund_info
File Created: Thursday, 13th May 2021 11:04:55 am
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2021 Camel Lu
'''
import time
import datetime
import os
import sys
from pprint import pprint
sys.path.append('../')
sys.path.append(os.getcwd() + '/src')
from utils.index import get_season_index
from sql_model.fund_query import FundQuery


class FundStatistic:
    def __init__(self):
      # 统计上一个季度
        last_quarter_time = time.localtime(time.time() - 3 * 30 * 24 * 3600)
        # time.strftime("%m-%d", last_quarter_time)
        year = time.strftime("%Y", last_quarter_time)
        date = time.strftime("%m-%d", last_quarter_time)
        index = get_season_index(date)
        quarter_index = year + '-Q' + str(index)
        self.quarter_index = quarter_index
        self.each_query = FundQuery()

    def all_stock_fund_count(self, *, quarter_index=None, fund_code_pool=None, filter_count=100):
        """查询某一个季度基金的十大持仓，并对持仓股票进行汇总统计，并根据filter_count进行过滤

        Args:
            quarter_index (string, optional): [description]. Defaults to None.取self.quarter_index
            fund_code_pool (string[], optional): [description]. Defaults to None. 传入查询的基金池，为None默认查询全部
            filter_count (int, optional): [description]. Defaults to 100. 过滤门槛，过滤掉一些持仓低的股票

        Returns:
            tuple[]: 每只股票的名称，以及对应持仓基金个数的list
        """

        quarter_index = quarter_index if quarter_index else self.quarter_index
        results = self.each_query.select_top_10_stock(
            quarter_index,
            fund_code_pool
        )
        code_dict = dict()
        for result in results:
            # print(result)
            for index in range(1, len(result), 2):
                code = result[index]
                name = result[index + 1]  # 仅以股票名称为key，兼容港股，A股
                # key = str(code) + '-' + str(name)

                key = str(name)
                if(key in code_dict and code != None):
                    code_dict[key] = code_dict[key] + 1
                else:
                    code_dict[key] = 1
        filer_dict = dict()

        for key, value in code_dict.items():  # for (key,value) in girl_dict.items() 这样加上括号也可以
            if value > filter_count and key != None:
                filer_dict[key] = value
                # print(key + ":" + str(value))
        list = sorted(filer_dict.items(), key=lambda x: x[1], reverse=True)
        return list

    # 分组查询特定股票的每个季度基金持有总数
    def item_stock_fund_count(self, stock_name, fund_code_pool=None):
        return self.each_query.select_special_stock_fund_count(stock_name, fund_code_pool)

    def select_fund_pool(self, *, morning_star_rating_5="", morning_star_rating_3="", **args):
        # print("morning_star_rating_5", morning_star_rating_5)
        # print("morning_star_rating_3", morning_star_rating_3)
        # print("args", args)
        # morning_star_rating_5 = 5

        return self.each_query.select_certain_condition_funds(
            morning_star_rating_5=morning_star_rating_5,
            morning_star_rating_3=morning_star_rating_3,
            **args
        )

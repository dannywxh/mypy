#!/usr/bin/python
# coding: UTF-8

"""This script parse stock info"""

import tushare as ts


def get_all_price(code_list):
    '''''process all stock'''
    df = ts.get_realtime_quotes(STOCK)
    print df


if __name__ == '__main__':
    STOCK = ['600219',  ##南山铝业
             '000002',  ##万  科Ａ
             '000623',  ##吉林敖东
             '000725',  ##京东方Ａ
             '600036',  ##招商银行
             '601166',  ##兴业银行
             '000792']  ##盐湖股份

    get_all_price(STOCK)
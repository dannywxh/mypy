#!/usr/bin/python
# coding: UTF-8

"""This script parse stock info"""

import tushare as ts


def get_all_price(code_list):
    '''''process all stock'''
    df = ts.get_realtime_quotes(STOCK)
    print df

#-*-coding=utf-8-*-
__author__ = 'rocky'
'''
http://30daydo.com
weigesysu@qq.com
'''
#获取破指定天数内的新高 比如破60日新高

import datetime

info=ts.get_stock_basics()

def loop_all_stocks():
    for EachStockID in info.index:
         if is_break_high(EachStockID,60):
             print "High price on",
             print EachStockID,
             print info.ix[EachStockID]['name'].decode('utf-8')



def is_break_high(stockID,days):
    end_day=datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)
    days=days*7/5
    #考虑到周六日非交易
    start_day=end_day-datetime.timedelta(days)

    start_day=start_day.strftime("%Y-%m-%d")
    end_day=end_day.strftime("%Y-%m-%d")
    df=ts.get_h_data(stockID,start=start_day,end=end_day)

    period_high=df['high'].max()
    #print period_high
    today_high=df.iloc[0]['high']
    #这里不能直接用 .values
    #如果用的df【：1】 就需要用.values
    #print today_high
    if today_high>=period_high:
        return True
    else:
        return False



if __name__ == '__main__':
    STOCK = ['600219',  ##南山铝业
             '000002',  ##万  科Ａ
             '000623',  ##吉林敖东
             '000725',  ##京东方Ａ
             '600036',  ##招商银行
             '601166',  ##兴业银行
             '000792']  ##盐湖股份

    #get_all_price(STOCK)

    loop_all_stocks()




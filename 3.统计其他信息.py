'''
将医生填写的表格合并进实验数据中,形成新的excel文件
'''
import csv

import pandas as pd
import os
import numpy as np

import re
path = r'D:\实验程序\睡眠测试\exp_1\data'
os.chdir(path)

#读取两个表格
def read_excel():
    csv1 = pd.read_excel('数据合并.xlsx',sheet_name='汇总统计')
    csv2 = pd.read_excel('睡眠障碍信息表.xlsx',sheet_name='Sheet1',usecols=['姓名','性别','年龄','病史','用药情况'])
    csv2['PQSI'] = np.nan        #增加一列空，给下一个程序做判断
    return csv1,csv2

#表格信息合并
def match(dfa,dfb):
    dfa['被试'] = dfa['被试'].str.extract(r'([\u4e00-\u9fa5()（）]+)')  #str是pandas的字符串阅读工具,用extract写正则的时候要记得里面要用括号抓取
    csv3 = pd.merge(dfa,dfb,how='left',left_on='被试',right_on='姓名')
    # print(csv3)
    return csv3

def save(df):
    with pd.ExcelWriter('医生数据汇总.xlsx',mode='w',engine='openpyxl') as f:
        df.to_excel(f,sheet_name='汇总统计',index=False)

def search():
    csv = pd.read_excel('医生数据汇总.xlsx')
    csv.info()
    print(csv['性别'].value_counts())

if __name__ == '__main__':
    res = read_excel()
    print(res[0])
    print(res[1])
    res2 = match(res[0],res[1])
    save(res2)
    # search()
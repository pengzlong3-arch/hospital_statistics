'''
把SDS,SAS问卷手动按表格名字顺序录入
'''
import csv
import os
import pandas as pd
import numpy as np
from pandas.core import col
from statsmodels.miscmodels import count

from 计分 import score


path = r'D:\实验程序\睡眠测试\exp_1\data'
os.chdir(path)
class Method():
    def __init__(self):
        self.csv = None
        self.new_data = []
    #读取表格信息
    def read(self):
        #第一次录入时
        if not os.path.exists('数据最终汇总.xlsx'):
            self.csv = pd.read_excel('医生数据汇总.xlsx',sheet_name='汇总统计')
            self.csv = self.csv.iloc[:,:12]          #去除掉原表的一些无用信息
            self.csv['标记'] = np.nan                #设计一列新的标记,来确定本行有没有录入,在录一半退出后重新录入有作用
            self.csv.to_excel('数据最终汇总.xlsx',sheet_name='汇总统计',index=False)
        #后面再录入时
        else:
            self.csv = pd.read_excel('数据最终汇总.xlsx',sheet_name='汇总统计')
        # print(self.csv)
        #获得每一行的index
        for i in range(len(self.csv.values)):
            # print(i)
            df = self.csv.iloc[i, 0]
            print(self.csv.iloc[i,12])           #第12列即为self.csv['标记']
            #如果第13列PSQI是空的，才录入，不是就跳过
            if np.isnan(self.csv.iloc[i,12]):     #千万不要写XXX == np.nan
                print(f'当前录入的名字是{df}')
                self.type_in()
                self.csv.iloc[i, 12] = 1
            else:
                continue
            #退出保存
            note = input('是否退出y/n?\n')
            if note.strip().upper() == 'Y':
                self.save()
                return
    #调用计分方法
    def type_in(self):
        df = score()
        self.new_data.append(df)

    #保存数据
    def save(self):
        #先将录入的数据合并
        if len(self.new_data) >= 2:
            new = pd.concat([i for i in self.new_data],axis='rows')
        else:
            new = self.new_data[0]
        #建一个新的表格,后面方便结合
        if not os.path.exists('PQSI原始数据汇总.xlsx'):
            new.to_excel('PQSI原始数据汇总.xlsx',sheet_name='汇总统计',index=False)
            new_pqsi = pd.read_excel('PQSI原始数据汇总.xlsx',sheet_name='汇总统计')
        else:
            old_pqsi = pd.read_excel('PQSI原始数据汇总.xlsx', sheet_name='汇总统计')
            new_pqsi = pd.concat([old_pqsi,new],axis='rows')
            new_pqsi.to_excel('PQSI原始数据汇总.xlsx',sheet_name='汇总统计',index=False)

        csv_final = pd.merge(self.csv.iloc[:,0:13],new_pqsi,left_on='姓名',right_on='姓名',how='left')
        print(csv_final)
        csv_final.to_excel('数据最终汇总.xlsx',index=False,sheet_name='汇总统计')






if __name__ == '__main__':
    res = Method()
    res.read()
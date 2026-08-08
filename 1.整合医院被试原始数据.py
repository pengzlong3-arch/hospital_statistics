'''
正则提取实验数据,组合成原始数据的excel文件
'''

import pandas as pd
import os
import time
import re

#去到目标data文件夹进行,做准备
path = r'D:\实验程序\睡眠测试\exp_1\data'
os.chdir(path)
print(os.getcwd())

class NameTime():
    def __init__(self):
        self.path = r'D:\实验程序\睡眠测试\exp_1\data'
        self.name = None         #文件原本的名字
        self.creat_name = None   #文件后来取的名字
        self.create_time = None  #文件建立的时间
    def find_csv_name_and_time(self):
        count = 0
        with pd.ExcelWriter('数据整理1.xlsx', engine='openpyxl') as f:   #保持工作表持续打开(f在.save里面才用到)
            files = os.listdir(self.path)       #获取文件夹里所有文件
            file_sorted_time =  sorted(files, key=lambda x:os.stat(x).st_ctime)  #os.stat(x)找x文件的创建时间
            for name in file_sorted_time:   #为了找时间,需要用到.stat(),.strftime(),.localtime().st_ctime()
                try:
                    if name.endswith('.csv') and re.search(r'[\u4e00-\u9fa5()]+', name):
                        find_time = os.stat(name)
                        self.create_time = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(find_time.st_ctime))
                        self.name = name
                        self.creat_name = re.search(r'[\u4e00-\u9fa5A-Za-z()（）0-9]+', name).group(0) + self.create_time
                        to_Trial = Trial(self.name)    #在name_time内部调用Trial类的方法

                        #计算够不够96条数据
                        to_Trial.coun()
                        # #保存数据
                        to_Trial.save(f, self.creat_name)
                        count += 1

                        # print(self.creat_name)
                        # print(self.name)
                except Exception as e:
                    print(e)
        print(count)



class Trial():
    def __init__(self,x):
        self.start = 0
        self.end = 0
        self.lst = []   #为了把待会的两个索引值储存
        try:
            self.df = pd.read_csv(x, sep=',', usecols = ['condition',
                                                       'key_resp_2.corr','key_resp_2.rt'])
        except:
            self.df = pd.read_csv(x, sep=',', encoding= 'gbk',
                                  usecols=['condition','key_resp_2.corr', 'key_resp_2.rt'])
        self.df.rename(
            columns={'condition': '条件', 'key_resp_2.corr': '正确值', 'key_resp_2.rt': '反应时'},
            inplace=True)
        self.new_df = None   #真正的dataframe
        # print(self.df)
    #计算够不够96条数据
    def coun(self):
        for i in range(self.df.shape[0]):   #从第一行开始遍历到最后一行
            self.start = self.end
            if pd.isna(self.df.iloc[i,:]).all():  #判断这一行cell是不是都是空值
                self.end = i      #加减一是为了刚好取到空行后或空行前的值
                # print(self.start)
                # print(self.end)
                if self.end - self.start -1 == 96:   #过滤掉没有96行的数据
                    self.lst.append([self.start +1,self.end])    #装两个数据进列表中,避免空行,一个加1
        # print(self.lst)
        self.concat()
    #合并两次实验数据
    def concat(self):
        lst = []
        for item in self.lst:
            if item:
                df = self.df.iloc[item[0]:item[1],:]
                lst.append(df)
        # print(lst)
        #111.原始数据
        if len(lst) == 2:
            self.new_df = pd.concat([lst[0],lst[1]],axis='rows')    #axis设置以列合并
            self.deal_data() #处理缺失值

        # print(self.new_df)
        # print(self.new_df.groupby(['条件']).agg({'正确值':'mean','反应时':'mean'}))
        # print(self.new_df.describe())

    def deal_data(self):   #用均值填补缺失值
        try:
            print(self.new_df.loc[:,'反应时'])
            print(type(self.new_df.loc[:,'反应时']))
            print(f'均值是: {self.new_df.loc[:,'反应时'].mean()}')
            self.new_df.fillna({'反应时': self.new_df.loc[:,'反应时'].mean()}, inplace = True)   #用均值代替缺失值
            print(self.new_df.loc[:, '反应时'])
        except:
            pass


    #保存数据
    def save(self,f, y):
        # print('-'*23)
        # print(y)
        # print('-'*23)
        # # self.df.to_csv('覃燕芬数据整理.csv')
        if self.new_df is not None:    #这个有可能不是dataframe对象, 只是一个None
            try:
                self.new_df.to_excel(f,sheet_name= y,index= False)   #index取消, sheet表会更好看
            except Exception as e:
                print(e,y)


if __name__ == '__main__':
    res = NameTime()
    result = res.find_csv_name_and_time()

    # res = Trial('黄新明3_untitled_2026-05-27_09h06.28.960.csv')
    # res.coun()
    # res.save()

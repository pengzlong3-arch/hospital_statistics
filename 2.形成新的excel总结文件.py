'''
把原始数据的excel文件,统计成汇合excel文件
'''
import pandas as pd
import os


#去到目标文件夹操作
os.chdir(r'D:\实验程序\睡眠测试\exp_1\data')

# df = pd.read_excel(r'数据整理.xlsx', sheet_name='黄新明32026-05-27 09-15-57')
# # print(df)
# print(df.groupby('条件').get_group('A'))
# res = df.groupby('条件', as_index=False).agg({'正确值': 'mean','反应时':'mean'})
# res.sort_values(by='条件', key = lambda x : x.str.len(), ascending = True, inplace=True)
# print(res)
# print(len(res['条件']))
# new_df1 = pd.DataFrame({'A反应时':[res.loc[0,'反应时']],
#                         'V反应时':[res.loc[1,'反应时']],
#                         'AV反应时':[res.loc[2,'反应时']]
#                         })
# new_df2 = pd.DataFrame({'A正确率':[res.loc[0,'正确值']],
#                         'V正确率':[res.loc[1,'正确值']],
#                         'AV正确率':[res.loc[2,'正确值']]
#                         })
# print(new_df1)
# print(new_df2)

class Sort():
    time = []     #类属性
    corr = []
    all_ = []
    def __init__(self,file,sheet_name = None):
        self.file = file    #所读文件名字
        self.sheet = sheet_name   #所读的sheet

    #开始读表,排顺序
    def read(self):
        df = pd.read_excel(self.file, sheet_name=self.sheet)
        res = df.groupby('条件', as_index=False).agg({'正确值':'mean','反应时':'mean'})
        #排序,获得A,V,AV顺序
        res.sort_values(by='条件', key = lambda x : x.str.len(), ascending = True, inplace=True,ignore_index=True)
        print(res)
        new_df_time = pd.DataFrame({'被试': self.sheet,
                                        'A反应时': [res.loc[0, '反应时']],
                                         'V反应时': [res.loc[1, '反应时']],
                                        'AV反应时': [res.loc[2, '反应时']]
                                         })
        Sort.time.append(new_df_time)    #调用的是类属性,共享的

        new_df_corr = pd.DataFrame({'被试': self.sheet,
                                        'A正确率':[res.loc[0,'正确值']],
                                         'V正确率':[res.loc[1,'正确值']],
                                        'AV正确率':[res.loc[2,'正确值']]
                                         })
        Sort.corr.append(new_df_corr)

        all_df = pd.concat([new_df_time,new_df_corr.iloc[:,1:]],axis='columns')
        print(all_df)
        Sort.all_.append(all_df)

    def save(self):
        with pd.ExcelWriter('数据合并.xlsx', engine='openpyxl') as f:
            df_corr = pd.concat([item for item in Sort.corr], axis='rows')    #这里面调用类属性
            df_time = pd.concat([item for item in Sort.time], axis='rows')
            df_all = pd.concat([item for item in Sort.all_],axis='rows')
            df_corr.to_excel(f,sheet_name = '正确率统计', index = False)
            df_time.to_excel(f,sheet_name = '反应时统计', index = False)
            df_all.to_excel(f,sheet_name='汇总统计',index=False)

if __name__ == '__main__':
    sheet_names = pd.ExcelFile('数据整理1.xlsx').sheet_names
    # print(sheet_names)
    count = 0
    for i in sheet_names:
        res = Sort('数据整理1.xlsx',i)
        res.read()
        count+= 1
    res.save()
    print(count)

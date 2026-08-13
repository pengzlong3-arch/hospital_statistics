'''
进行数据处理
    把正确率低于0.8的剔除
    把失眠根据总分划分为两类
    性别男女改成0，1编码
'''
import pandas as pd
import numpy as np

import os

os.chdir(r'D:\实验程序\睡眠测试\exp_1\data')
def deal_general():
    #1.加载数据
    csv = pd.read_excel('数据最终汇总.xlsx',sheet_name='汇总统计')
    # print(csv)
    # print(csv.info())
    #1.1数据预处理
    col = [i for i in range(0, 7)] + [8,9] + [38,39,40]
    #1.2删除还没录入的数据
    use_col = csv.iloc[:,col].dropna(subset=['总分','SAS','SDS'], axis='rows',how='any')
    #1.3只选取正确率大于80%的
    use_col1 = use_col.query('A正确率>0.8 & V正确率>0.8 &AV正确率>0.8')
    nouse_col =use_col.query('A正确率<=0.8 & V正确率<=0.8 &AV正确率<=0.8')
    print(f'剔除的数据{nouse_col}')
    #1.4把总分划分为失眠和非失眠两类,0为无失眠,1为有失眠
    use_col1['总分'] = pd.cut(use_col1['总分'],bins=[0,9,22],labels=[0,1])   #0无失眠,1失眠
    use_col1['性别'] = use_col1['性别'].map({'男':1,'女':0})
    #1.5把总分移动到最后一列
    score_col = use_col1.pop('总分')
    use_col1['总分'] = score_col
    #全部rename
    use_col1.rename(inplace=True,columns={
        '被试':'sub',
        'A反应时':'A_t',
        'V反应时':'V_t',
        'AV反应时':'AV_t',
        'A正确率': 'A_corr',
        'V正确率': 'V_corr',
        'AV正确率': 'AV_corr',
        '性别':'gender',
        '年龄':'age',
        '总分':'score'
    })
    print(use_col1)
    print(use_col1.info())
    # print(use_col.describe())
    use_col1.to_csv('已预处理的数据.csv',index=False)
    use_col1.describe().to_csv('描述统计.csv',index=True)
    print(use_col1.describe())
    print(use_col1['gender'].value_counts())


if __name__ == '__main__':
    #数据预处理
    deal_general()

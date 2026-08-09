'''
逻辑回归分析
'''
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
import os

os.chdir(r'D:\实验程序\睡眠测试\exp_1\data')

def deal_logistic():
    # 1.1加载已预处理的数据
    csv = pd.read_csv('已预处理的数据.csv',index_col=False)
    print(csv)
    print(csv.info())
    x = csv.iloc[:,1:11]
    y = csv.iloc[:,11]
    print(x)
    print(y)
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=5,stratify=y)
    print(x_train.info())
    # print(y_train.dtype)
    #2.1特征工程
    #2.1.1特征数据先划分连续列和分类列
    continue_col = [i for i in range(0,6)] + [i for i in range(7,10)]
    category_col = [6]
    #2.1.2连续数据标准化及类别数据编码
    preprocessor = ColumnTransformer(
        transformers = [
            ('num',StandardScaler(),continue_col),
            ('cat',OneHotEncoder(),category_col)
        ]
    )
    x_train = preprocessor.fit_transform(x_train)
    x_test = preprocessor.transform(x_test)

    #2.1.2标签转化成str
    y_train.astype('str')
    y_test.astype('str')

    #3.建立模型对象
    estimator = LogisticRegression()
    #3.1模型分析
    estimator.fit(x_train,y_train)
    y_pre = estimator.predict(x_test)
    #4.模型评估
    print(y_test)
    print(y_pre)
    print(f'分类评估报告{classification_report(y_test,y_pre)}')
    print(f'变量{x.columns}')
    print(f'系数{estimator.coef_}')
    print(f'负例,正例{estimator.classes_}')

if __name__ == '__main__':
    deal_logistic()
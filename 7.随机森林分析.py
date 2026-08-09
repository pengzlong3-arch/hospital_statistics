'''
随机森林分析
'''
import pandas as pd
import shap
import os
import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
os.chdir(r'D:\实验程序\睡眠测试\exp_1\data')

def random():
    csv = pd.read_csv('已预处理的数据.csv',index_col=False)
    print(csv.info())
    print(csv.describe())
    x = csv.iloc[:,1:11]
    y = csv.iloc[:,11]
    #划分数据集
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=8,stratify=y)
    # # 建立随机森林
    # estimator = RandomForestClassifier()
    # #网格搜索交叉验证+最佳模型拟合
    # para = {'n_estimators':[90,100,120,130,140],'max_depth':[3,5,7,9]}
    # gs_estimator = GridSearchCV(estimator,param_grid=para,cv=5)
    # gs_estimator.fit(x_train,y_train)
    # print(f'最佳正确率{gs_estimator.best_score_}')
    # print(f'最佳参数组合为: {gs_estimator.best_params_}')
    # print(f'最佳组合准确率为{gs_estimator.score(x_test,y_test)}')

    #模型拟合
    estimator_final = RandomForestClassifier(max_depth=3,n_estimators=120,random_state=1)
    estimator_final.fit(x_train,y_train)
    y_pre = estimator_final.predict(x_test)
    print(f'分类评估报告{classification_report(y_test,y_pre)}')
    print(f'使用的特征{estimator_final.n_features_in_}')

    #评估系数
    explainer = shap.TreeExplainer(estimator_final)
    shap_values = explainer.shap_values(x_test)
    print(shap_values[:,:,1].shape)       #shap_values 是三维数组
    print(shap_values[0].shape)
    print(x_test.shape)
    # print(x_test.isnull().sum())

    #画图
    plt.figure(figsize=(10, 5), dpi=160)
    shap.summary_plot(shap_values[:,:,1],x_test,show=False)
    plt.savefig('蜂群摘要图.png')





if __name__ == '__main__':
    random()
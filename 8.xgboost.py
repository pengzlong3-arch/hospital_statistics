'''

'''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os
from sklearn.metrics import classification_report
import xgboost as xgb
import matplotlib.pyplot as plt
import shap

os.chdir(r'D:\实验程序\睡眠测试\exp_1\data')

def xgb_classify():
    #1.读取csv文件
    csv = pd.read_csv('已预处理的数据.csv',index_col=False)
    # enable_categorical=False 时不能转category，保持数值型即可
    print(csv.describe())
    print(csv.info())
    x = csv.iloc[:,1:11]
    y = csv.iloc[:,11]
    #拆分训练集测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=3,stratify=y)
    estimator = xgb.XGBClassifier(
        enable_categorical=False,  # interventional模式下不支持categorical
        max_depth=3,
        n_estimators=100,
        subsample=.8,
        colsample_bylevel=.8,
        colsample_bynode=.8,
        colsample_bytree=.8,
        learning_rate=0.01,
        random_state=9,
        objective='binary:logistic'  # 双分类.
    )
    estimator.fit(x_train, y_train)
    y_pre = estimator.predict(x_test)
    print(x_test.head())
    print(f'分类评估报告{classification_report(y_test,y_pre)}')

    #评估系数（probability空间 + interventional，让瀑布图直接显示概率）
    explainer = shap.TreeExplainer(estimator, x_train.iloc[:100],
                                   model_output='probability',
                                   feature_perturbation='interventional')
    shap_values = explainer.shap_values(x_test)
    print(shap_values[1].shape)       #这里shap_values 是二维数组
    print(shap_values)

    print(x_test.shape)

    #画图
    plt.figure(figsize=(10, 5), dpi=160)
    shap.summary_plot(shap_values,x_test,show=False)
    plt.tight_layout()
    plt.savefig('蜂群摘要图_xbg.png')
    plt.close()

    shap.dependence_plot('gender',shap_values,x_test,show=False,interaction_index=None) #关掉颜色条,避免干扰
    plt.tight_layout()               #让图像更紧凑,让文字显示
    plt.savefig('性别类蜂群_xgb.png')
    plt.close()
    # plt.show()

    #画瀑布图尝试解释单个样本
    print('*'*23)
    print(shap_values[1])
    print(y_train.unique())
    print(y_pre)
    # print(y_test.to_numpy())
    # print(x_test.iloc[1,:])
    # print(explainer.expected_value)
    feature_names = x_test.columns
    # print(feature_names)
    # print(f'该测试集的列表\n{x_test}')

    prob_lst = []
    for num in range(x_test.shape[0]):
        # SHAP已在概率空间，raw_sum 直接等于 P(1)
        prob = explainer.expected_value + shap_values[num].sum()
        exp = shap.Explanation(
            values=shap_values[num],  #看第一个样本
            base_values=explainer.expected_value,   #看正类(失眠)的基值
            data=x_test.iloc[num,:],
            feature_names=feature_names
        )
        plt.figure(figsize=(20, 10), dpi=160)
        shap.waterfall_plot(exp,show=False)
        plt.title(f'Xgb_Subject{num}')
        plt.tight_layout()
        plt.savefig(f'xgboost样本{num}的瀑布图.png')
        # plt.show()
        prob_lst.append(prob)
    print(prob_lst)
    print(estimator.predict_proba(x_test))



if __name__ == '__main__':
    xgb_classify()
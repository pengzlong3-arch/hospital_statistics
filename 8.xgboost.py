'''

'''
import pandas as pd
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
    csv['gender'] = csv['gender'].astype('category')       #转成分类更严谨
    csv['score'] = csv['score'].astype('category')
    print(csv.describe())
    print(csv.info())
    x = csv.iloc[:,1:11]
    y = csv.iloc[:,11]
    #拆分训练集测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=21, stratify=y)
    estimator = xgb.XGBClassifier(
        enable_categorical= True,
        max_depth=3,
        n_estimators=120,
        learning_rate=0.01,
        random_state=8,
        objective='binary:logistic'  # 双分类.
    )
    estimator.fit(x_train, y_train)
    y_pre = estimator.predict(x_test)
    print(f'分类评估报告{classification_report(y_test,y_pre)}')

    #评估系数
    explainer = shap.TreeExplainer(estimator)
    shap_values = explainer.shap_values(x_test)
    print(shap_values[1].shape)       #这里shap_values 是二维数组
    print(shap_values.shape)

    # print(x_test.shape)

    #画图
    plt.figure(figsize=(10, 5), dpi=160)
    shap.summary_plot(shap_values,x_test,show=False)
    shap.dependence_plot('gender',shap_values,x_test,show=False,interaction_index=None) #关掉颜色条,避免干扰
    # plt.savefig('蜂群摘要图_xgb.png')
    plt.show()

    #画瀑布图尝试解释单个样本
    print('*'*23)
    print(shap_values[1])
    print(y_pre[1])
    print(x_test.iloc[1,:])
    print(explainer.expected_value)
    feature_names = x_test.columns
    print(feature_names)
    num = 1
    exp = shap.Explanation(
        values=shap_values[num],  #看第一个样本
        base_values=explainer.expected_value,   #看正类(失眠)
        data=x_test.iloc[num,:],
        feature_names=feature_names
    )
    plt.figure(figsize=(20, 10), dpi=160)
    shap.waterfall_plot(exp,show=False)
    plt.tight_layout()
    # plt.savefig(f'样本{num}的瀑布图.png')
    plt.show()


if __name__ == '__main__':
    xgb_classify()
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
    csv['gender'] = csv['gender'].astype('category')       #转成分类更严谨
    csv['score'] = csv['score'].astype('category')
    print(csv.info())
    print(csv.describe())
    x = csv.iloc[:,1:11]
    y = csv.iloc[:,11]
    print(y.info())

    #划分数据集
    # #试着不用正确率
    # cols = [i for i in x.columns if i not in ['A_corr','V_corr','AV_corr']]
    # print(cols)
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=3,stratify=y)
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
    estimator_final = RandomForestClassifier(max_depth=3,n_estimators=100,random_state=3)
    estimator_final.fit(x_train,y_train)
    y_pre = estimator_final.predict(x_test)
    print(f'分类评估报告{classification_report(y_test,y_pre)}')
    print(f'使用的特征{estimator_final.n_features_in_}')

    #评估系数
    explainer = shap.TreeExplainer(estimator_final)
    shap_values = explainer.shap_values(x_test)
    # print(shap_values[:,:,1].shape)       #shap_values 在这里是三维数组
    # print(shap_values[0].shape)
    # print(shap_values.shape)
    # print(x_test.shape)
    # print(x_test.isnull().sum())

    #画图
    plt.figure(figsize=(10, 5), dpi=160)
    shap.summary_plot(shap_values[:,:,1],x_test,show=False)
    plt.tight_layout()
    plt.savefig('蜂群摘要图_随机森林.png')
    plt.close()

    shap.dependence_plot('gender',shap_values[:,:,1],x_test,show=False,interaction_index=None) #关掉颜色条,避免干扰
    plt.tight_layout()               #让图像更紧凑,让文字显示
    plt.savefig('性别类蜂群_随机森林.png')
    plt.close()

    # plt.show()

    #画瀑布图尝试解释单个样本
    print('*'*23)
    print(shap_values[2,1])
    print('*' * 23)
    print(y_pre[1])     #查看第一类
    print('*' * 23)
    print(x_test.iloc[1,:])
    print('*' * 23)
    print(explainer.expected_value)
    feature_names = x_test.columns
    # print(feature_names)
    print(f'该测试集集的列表\n{x_test}')

    for num in range(x_test.shape[0]):
        exp = shap.Explanation(
            values=shap_values[num,:,1],  #查看正类的第一个样本
            base_values=explainer.expected_value[1],   #看正类(失眠)
            data=x_test.iloc[num,:],
            feature_names=feature_names
        )
        plt.figure(figsize=(20, 10), dpi=160)
        shap.waterfall_plot(exp,show=False)
        plt.title(f'Forest_Subject{num}')
        plt.tight_layout()
        plt.savefig(f'随机森林样本{num}的瀑布图.png')
        # plt.show()





if __name__ == '__main__':
    random()
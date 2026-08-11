'''
逻辑回归分析
'''
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV,StratifiedKFold
from sklearn.metrics import classification_report,auc,roc_curve
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
import  matplotlib.pyplot as plt
from numpy import interp
import statsmodels.api as sm              #描述逻辑回归系数p值
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
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=3,stratify=y)
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
    estimator = LogisticRegression(max_iter=1000)
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


    #插入:计算逻辑回归系数
    x_train_sm = sm.add_constant(x_train)   #手动添加截距
    #构建逻辑回归模型
    logit_model = sm.Logit(y_train,x_train)
    result = logit_model.fit(disp=0)  #disp=0关闭迭代打印
    #打印结果(系数,p值,or,95置信区间)
    print('*'*23)
    print(result.pvalues)
    print('*'*23)
    print(np.exp(result.params))       #or
    print(result.params)       #or
    print('*'*23)
    print(np.exp(result.conf_int()))  #95%置信区间
    print('*'*23)

    #5.可视化画图

    # #5.1找到负类正类的概率
    # y_proba = estimator.predict_proba(x_test)
    # print(y_proba)
    # #5.2取到正类
    # y_score = y_proba[:,1]
    # print(y_score.shape)
    # print(y_proba.shape)
    # #5.3计算roc点
    # fpr,tpr,thresholds = roc_curve(y_test,y_score)
    # #5.4计算auc值
    # roc_auc = auc(fpr,tpr)
    # #5.5可视化
    # plt.figure(figsize=(10,5),dpi=160)
    # plt.plot(fpr,tpr,color='red',lw=2,label=f'ROC curve(AUC = {roc_auc:.3f})')
    # plt.plot([0,1],[0,1],color='gray',lw=1.5,linestyle='--')
    # plt.xlim([0.0,1.0])
    # plt.ylim([0.0,1.05])
    # plt.xlabel('False positive rate')
    # plt.ylabel('True positive rate')
    # plt.title('ROC')
    # plt.legend(loc='lower right')
    # # plt.savefig()
    # plt.show()

    #插入:计算k折来画出更平滑的roc曲线
    cv = StratifiedKFold(n_splits=3)
    mean_fpr = np.linspace(0,1,100)  #生成公共的x轴fpr值
    tprs = []
    aucs = []
    for index_train,index_test in cv.split(x,y):     #根据标签y做分层,返回所划分的训练集索引和验证集索引
        print(index_train)
        x_train_cv,x_test_cv = x.iloc[index_train],x.iloc[index_test]
        y_train_cv,y_test_cv= y.iloc[index_train],y.iloc[index_test]
        estimator.fit(x_train_cv,y_train_cv)         #根据每次划分做训练
        y_score_cv = estimator.predict_proba(x_test_cv) [:,1]      #计算负类正类的概率,然后取正类
        fpr,tpr,thresholds = roc_curve(y_test_cv,y_score_cv)       #计算画图所需要的值
        tprs.append(interp(mean_fpr,fpr,tpr))
        tprs[-1][0] = 0                      #强制让刚进去(最后)的点x设为0
        roc_auc = auc(fpr,tpr)
        aucs.append(roc_auc)
    mean_tpr = np.mean(tprs,axis=0)
    mean_tpr[-1] = 1                           #强制让最后一个点y=1
    mean_auc = auc(mean_fpr,mean_tpr)
    #可视化
    plt.figure(figsize=(10,5),dpi=160)
    plt.plot(mean_fpr,mean_tpr,color='red',lw=2,label=f'ROC curve(AUC = {mean_auc:.3f})')
    plt.plot([0,1],[0,1],color='gray',lw=1.5,linestyle='--')
    plt.xlim([0.0,1.0])
    plt.ylim([0.0,1.05])
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC')
    plt.legend(loc='lower right')
    plt.savefig('逻辑回归roc图')
    # plt.show()
if __name__ == '__main__':
    deal_logistic()
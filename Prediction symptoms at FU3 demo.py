#### linear regression ##### Python
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
#随机抽样200次，每次5折，产生1000个r
from sklearn.svm import SVR

def fold5(x, x_less, y):
    # 将数据拆成5份
    kf = KFold(n_splits=5, shuffle=True)
    x_train_list=[]
    xLess_train_list=[]
    y_train_list=[]
    x_test_list=[]
    xLess_test_list=[]
    y_test_list=[]
    for i, (train_index, test_index) in enumerate(kf.split(x)):
        print("第{}折".format(i))
        # print(train_index)
        # print(test_index)
        # print(x[test_index])
        x_train_list.append(x[train_index])
        y_train_list.append(y[train_index])
        xLess_train_list.append(x_less[train_index])
        x_test_list.append(x[test_index])
        xLess_test_list.append(x_less[test_index])
        y_test_list.append(y[test_index])
    return x_train_list, y_train_list, x_test_list, y_test_list, xLess_train_list, xLess_test_list


data=pd.read_excel("ABCD prediction.xlsx")
data=data.dropna(subset=['SCORE_0.05'])
#data=data[data['imgincl_t1w_include.x'] != 0]
#data=data[data['imgincl_t1w_include.y'] != 0]
##### FU2 没必要单独考虑，因为delta包含了FU2的信息，我们强调的是脑的发育
##### BL和delta没必要同时考虑，因为共线性太高了。
##### PRS 可以试试
##### 环境 认知，功能，动机这些没有delta的变化

data_X=data[["cov_interview_age", "cov_demo_sex_v2", "cov_demo_comb_income_v2", "cov_demo_prnt_ed_v2", 'SCORE_0.05',"ADHD_Total_BL",
            "smri_thick_cdk_cdmdfrrh_delta_y", "smri_thick_cdk_sufrlh_delta_y", "smri_thick_cdk_sufrrh_delta_y", "smri_vol_scs_hpuslh_delta_y", 
            "smri_thick_cdk_ptcaterh_delta_y","smri_thick_cdk_insularh_delta_y"]]
data_X_less=data[["cov_interview_age", "cov_demo_sex_v2", "cov_demo_comb_income_v2", "cov_demo_prnt_ed_v2", 'SCORE_0.05',"ADHD_Total_BL",
            "smri_thick_cdk_cdmdfrrh.x", "smri_thick_cdk_sufrlh.x", "smri_thick_cdk_sufrrh.x", "smri_vol_scs_hpuslh.x", 
            "smri_thick_cdk_ptcaterh.x","smri_thick_cdk_insularh.x"]]
data_Y=data["ADHD_Total_FU3"]  # 设置Y变量 ADHD_Total_FU3  ADHD_Inattention_FU3  ADHD_Hyperactivity_FU3


#data_X=data[["cov_interview_age", "cov_demo_sex_v2", "cov_demo_comb_income_v2", "cov_demo_prnt_ed_v2", 'SCORE_0.05',"ADHD_Total_BL","All_Med"]]
#data_X_less=data[["cov_interview_age", "cov_demo_sex_v2", "cov_demo_comb_income_v2", "cov_demo_prnt_ed_v2", 'SCORE_0.05',"ADHD_Total_BL","All_Med"]]
#data_Y=data["ADHD_Inattention_FU3"]  # 设置Y变量 ADHD_Total_FU3  ADHD_Inattention_FU3  ADHD_Hyperactivity_FU3


result=pd.DataFrame()
for i in range(200):
    temp=dict()
    X_train_list, Y_train_list, X_test_list, Y_test_list, XLess_train_list, XLess_test_list=fold5(data_X.values, data_X_less.values, data_Y.values)
    for x_train, y_train, x_test, y_test, xLess_train, xLess_test in zip(X_train_list, Y_train_list, X_test_list, Y_test_list, XLess_train_list, XLess_test_list):
        reg = SVR(kernel='linear') # 线性回归
        reg.fit(x_train, y_train)
        regLess=SVR(kernel='linear') # 线性回归
        regLess.fit(xLess_train, y_train)
        print("训练系数:\n", reg.coef_) # 输出系数
        print(reg.predict(x_test).shape)
        print(y_test.shape)
        corr, pvalue=pearsonr(reg.predict(x_test), y_test)
        corrLess, pvalueLess=pearsonr(regLess.predict(xLess_test), y_test)
        temp["相关性系数"]=corr
        temp["显著性"]=pvalue
        print("相关性系数:", corr)
        print("显著性:", pvalue)
        temp["相关性系数Less"]=corrLess
        temp["显著性Less"]=pvalueLess
        result=result._append(temp, ignore_index=True)  

result.to_excel("20241120 SVR Model0 ABCD ADHD_Total_FU3 trajectory prediction.xlsx", index=False)  

# print(data_X.describe())
# print(type(data_X.values))


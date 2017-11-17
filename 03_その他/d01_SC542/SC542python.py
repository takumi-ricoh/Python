# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 14:24:52 2017

@author: p000495138
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sn
data = pd.read_csv("DaiquriSC542他20170713.csv",engine="python")

"""-----全データ-----"""
#%%
data2 = data[["機種名","機番","訪問区分","製造年月","納入日","稼動月","保守実施日","顧客名","再訪問回数","条件","現象SC名称","ﾓﾉｸﾛ","再現性","処置","対象物","処置結果"]]
data2_MachineUnique = data2["機番"].value_counts()

#全稼動月ヒストグラム
#"""
plt.figure(1)
#ax1=data2["稼動月"].hist(bins=200)
ax1=data2["ﾓﾉｸﾛ"].hist(bins=200)
#ax1.set_xlabel("move_month")
ax1.set_xlabel("page")
ax1.set_ylabel("freq")
ax1.set_title("all")
#"""

#全scの件数
data2_SCUnique = data2["現象SC名称"].value_counts()
data2_UserUnique = data2["顧客名"].value_counts()

#%%SC間の関連調査

#全機番のSC状況
num541=[]
num542=[]
num543=[]
num544=[]
num545=[]
num551=[]
num553=[]
num554=[]
num_tsumari=[]
num_yogore=[]
num_jihada=[]
data3 = pd.DataFrame(data2["機番"].value_counts())
for idx,i in enumerate(data3.index):
    tmp = data2.loc[data2["機番"]==i,"現象SC名称"]
    num541.append(tmp[tmp=="SC541"].count())
    num542.append(tmp[tmp=="SC542"].count())
    num543.append(tmp[tmp=="SC543"].count())
    num544.append(tmp[tmp=="SC544"].count())
    num545.append(tmp[tmp=="SC545"].count())
    num551.append(tmp[tmp=="SC551"].count())
    num553.append(tmp[tmp=="SC553"].count())
    num554.append(tmp[tmp=="SC554"].count())
    num_tsumari.append(tmp[tmp=="用紙詰まり"].count())
    num_yogore.append(tmp[tmp=="汚れ･ﾎﾟﾁ汚れ"].count())
    num_jihada.append(tmp[tmp=="地肌汚れ"].count())
data3["SC541"]=num541
data3["SC542"]=num542
data3["SC543"]=num543
data3["SC544"]=num544
data3["SC545"]=num545
data3["SC551"]=num551      
data3["SC553"]=num553      
data3["SC554"]=num554      
data3["tsumari"]=num_tsumari      
data3["pochi"]=num_yogore      
data3["jihada"]=num_jihada    


#%%稼動月ごとの、枚数分布 / SC件数分布
#稼動月ファイル多
a1=data2[(0<=data2["稼動月"])&(5>data2["稼動月"])]
a2=data2[(5<=data2["稼動月"])&(10>data2["稼動月"])]
a3=data2[(10<=data2["稼動月"])&(15>data2["稼動月"])]
a4=data2[(15<=data2["稼動月"])&(20>data2["稼動月"])]
a5=data2[(20<=data2["稼動月"])&(25>data2["稼動月"])]
a6=data2[(25<=data2["稼動月"])&(30>data2["稼動月"])]
#各区分けの枚数分布
b1=a1["ﾓﾉｸﾛ"]
b2=a2["ﾓﾉｸﾛ"]
b3=a3["ﾓﾉｸﾛ"]
b4=a4["ﾓﾉｸﾛ"]
b5=a5["ﾓﾉｸﾛ"]
b6=a6["ﾓﾉｸﾛ"]
#各区分けの枚数合計
sum_b1=b1.sum()
sum_b2=b2.sum()
sum_b3=b3.sum()
sum_b4=b4.sum()
sum_b5=b5.sum()
sum_b6=b6.sum()
#各区分けのヒストグラム
"""
b1.hist(bins=200,alpha=0.5)
b2.hist(bins=200,alpha=0.5)
b3.hist(bins=200,alpha=0.5)
b4.hist(bins=200,alpha=0.5)
b5.hist(bins=200,alpha=0.5)
b6.hist(bins=200,alpha=0.5)
a=["~5month","~10month","~15month","~20month","~25month","~30month"]
plt.legend(a)
"""#各区分けの、機番ごと件数分布
c1=a1["機番"].value_counts()
c2=a2["機番"].value_counts()
c3=a3["機番"].value_counts()
c4=a4["機番"].value_counts()
c5=a5["機番"].value_counts()
c6=a6["機番"].value_counts()
#各区分けの枚数合計
sum_c1=c1.sum()
sum_c2=c2.sum()
sum_c3=c3.sum()
sum_c4=c4.sum()
sum_c5=c5.sum()
sum_c6=c6.sum()
#各区分けのヒストグラム
#"""
c1.hist(bins=20,alpha=0.5)
c2.hist(bins=20,alpha=0.5)
c3.hist(bins=20,alpha=0.5)
c4.hist(bins=20,alpha=0.5)
c5.hist(bins=20,alpha=0.5)
a=["~5month","~10month","~15month","~20month","~25month","~30month"]
plt.legend(a)
#"""
#%%各変数間の関係
data4=data3.drop("機番",axis=1)
cor_mat=np.corrcoef(data4.T)
#sn.heatmap(cor_mat,annot=True)

"""-----SC542データ-----"""
#%%sc542
sc542 = data2[data2["現象SC名称"]=="SC542"]
sc542_MachineUnique = sc542["機番"].value_counts()

#稼動月ヒストグラム
#"""
plt.figure(2)
#ax2=sc542["稼動月"].hist(bins=200)
ax2=sc542["ﾓﾉｸﾛ"].hist(bins=200)
#ax2.set_xlabel("move_month")
ax2.set_xlabel("page")
ax2.set_ylabel("freq")
ax2.set_title("sc542")
#"""
#顧客名ごと件数
sc542_UserUnique = sc542["顧客名"].value_counts()

#%%稼動月ごとの、枚数分布 / SC件数分布
#稼動月ファイル多
aa1=sc542[(0<=sc542["稼動月"])&(5>sc542["稼動月"])]
aa2=sc542[(5<=sc542["稼動月"])&(10>sc542["稼動月"])]
aa3=sc542[(10<=sc542["稼動月"])&(15>sc542["稼動月"])]
aa4=sc542[(15<=sc542["稼動月"])&(20>sc542["稼動月"])]
aa5=sc542[(20<=sc542["稼動月"])&(25>sc542["稼動月"])]
aa6=sc542[(25<=sc542["稼動月"])&(30>sc542["稼動月"])]
#各区分けの枚数分布
bb1=aa1["ﾓﾉｸﾛ"]
bb2=aa2["ﾓﾉｸﾛ"]
bb3=aa3["ﾓﾉｸﾛ"]
bb4=aa4["ﾓﾉｸﾛ"]
bb5=aa5["ﾓﾉｸﾛ"]
bb6=aa6["ﾓﾉｸﾛ"]
#各区分けの枚数合計
sum_bb1=bb1.sum()
sum_bb2=bb2.sum()
sum_bb3=bb3.sum()
sum_bb4=bb4.sum()
sum_bb5=bb5.sum()
sum_bb6=bb6.sum()
#各区分けのヒストグラム
"""
bb1.hist(bins=40,alpha=0.5)
bb2.hist(bins=40,alpha=0.5)
bb3.hist(bins=40,alpha=0.5)
bb4.hist(bins=40,alpha=0.5)
bb5.hist(bins=40,alpha=0.5)
bb6.hist(bins=40,alpha=0.5)
a=["~5month","~10month","~15month","~20month","~25month","~30month"]
plt.legend(a)
"""

#各区分けの、機番ごと件数分布
cc1=aa1["機番"].value_counts()
cc2=aa2["機番"].value_counts()
cc3=aa3["機番"].value_counts()
cc4=aa4["機番"].value_counts()
cc5=aa5["機番"].value_counts()
cc6=aa6["機番"].value_counts()
#各区分けの枚数合計
sum_cc1=cc1.sum()
sum_cc2=cc2.sum()
sum_cc3=cc3.sum()
sum_cc4=cc4.sum()
sum_cc5=cc5.sum()
sum_cc6=cc6.sum()
#"""
#各区分けのヒストグラム
cc1.hist(bins=20,alpha=0.5)
cc2.hist(bins=20,alpha=0.5)
cc3.hist(bins=20,alpha=0.5)
cc4.hist(bins=20,alpha=0.5)
cc5.hist(bins=20,alpha=0.5)
cc6.hist(bins=20,alpha=0.5)
a=["~5month","~10month","~15month","~20month","~25month","~30month"]
plt.legend(a)
#"""

#%%顧客種類
"""全SC"""
user_school_all = data2[data2["顧客名"].str.contains("学校")==True]
user_school_542 = sc542[sc542["顧客名"].str.contains("学校")==True]
user_factory_all = data2[data2["顧客名"].str.contains("工場")==True]
user_factory_542 = sc542[sc542["顧客名"].str.contains("工場")==True]
user_hospital_all = data2[data2["顧客名"].str.contains("病院")==True]
user_hospital_542 = sc542[sc542["顧客名"].str.contains("病院")==True]
user_logistics_all = data2[data2["顧客名"].str.contains("物流センター")==True]
user_logistics_542 = sc542[sc542["顧客名"].str.contains("物流センター")==True]
user_transport_all = data2[data2["顧客名"].str.contains("ヤマト運輸")==True]
user_transport_542 = sc542[sc542["顧客名"].str.contains("ヤマト運輸")==True]

# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:04:56 2019

@author: r00495138
"""


import re

#ライブラリ登録
form = "@f22@|[Sensor1|027:28.020 |Tar=,{1},Cur=,{2},Sen=,157,Air=,000,"#NG
#form2 = "@f22@|Sensor1|027:28.020 |Tar=,{1},Cur=,157,Sen=,157,Air=,000,"#NG
#form3 = "Sensor1027:28.020 Tar=,{1},Cur,157,Sen,157,Air,000,"#OK
#form4 = "f22|Sensor1|027:28.020 |Tar=,{1},Cur=,157,Sen=,157,Air=,000,"#NG
#form5 = "f22\|Sensor1\|027:28.020 \|Tar=,{1},Cur=,157,Sen=,157,Air=,000,"#OK
#form6 = "@f22@\|\[Sensor1\|027:28.020 \|Tar=,{1},Cur=,{2},Sen=,157,Air=,000," #OK
#form7 = re.escape(form) #NG
#form8 = r"@f22@|[Sensor1|027:28.020 |Tar=,{1},Cur=,157,Sen=,157,Air=,000,"#NG

def get_form(raw):
    form = raw.replace("|","\|")
    form = form.replace("[","\[")
    form = form.replace("$","\$")
    
    return form

form9 = get_form(form)

#検索対象
src =  "@f22@|[Sensor1|027:28.020 |Tar=,060,Cur=,157,Sen=,157,Air=,000,"#NG
#src2 =  "@f22@|Sensor1|027:28.020 |Tar=,060,Cur=,157,Sen=,157,Air=,000,"#NG
#src3 = "Sensor1027:28.020 Tar=,060,Cur,157,Sen,157,Air,000,"#OK
#src4 =  "f22|Sensor1|027:28.020 |Tar=,060,Cur=,157,Sen=,157,Air=,000,"#NG
#src5 =  "f22|Sensor1|027:28.020 |Tar=,060,Cur=,157,Sen=,157,Air=,000,"#OK
#src6 =  "@f22@|[Sensor1|027:28.020 |Tar=,060,Cur=,157,Sen=,157,Air=,000,"#OK

#パターン
re_form = re.sub(r'{\d+}', r'(\\w+)', form9)
print(f're_form is "{re_form}"')

#test_form = "@f22@|[Sensor1|027:28.020 |Tar=,060,Cur=,r'd{3}',Sen=,157,Air=,000,"
#test_form = "@f22@|[Sensor1|027:28.020 |Tar=,060,Cur=,r'd{3}',Sen=,157,Air=,000,"

#結果
#m = re.fullmatch(re_form, src)
m = re.search(re_form,src)
#m = re.fullmatch(test_form, src)
print(list(m.groups()))
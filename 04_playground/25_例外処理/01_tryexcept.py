# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 16:47:02 2020

@author: p000495138
"""

#%% try/except
try:
    #ValueErrorを出す
    x=int("x")

    #TypeErrorを出す
    #x=int([1,2,3])

    #ModuleNotFoundErrorを出す
    #import aaa
    
    #AssertErrorを出す
    #assert False
    
    #NameErrorを出す
    #prnt("word")
    
    #AttributeErrorを出す
    #print("word".float)
    
    #IndexErrorを出す
    #print([1,2,3][4])
    
    #KeyErrorを出す
    #print({"a":3}["b"])
    
    #SyntaxErrorを出す
    #print(1*/+3)
    
except ValueError: #ValueErrorが起きた場合：a="abc"とするとこれ 
    print("正しい値を入れてください")
except TypeError:
    print("タイプが違います")
except ModuleNotFoundError:
    print("そんなモジュールは無い")
except AssertionError:
    print("assertにひっかかったよ")
except NameError:
    print("そんな名前ない")
except AttributeError:
    print("そんな属性はない")
except IndexError:
    print("そこに値はない")
except KeyError:
    print("そんなキーはない")
except SyntaxError:
    print("文法がおかしい")
    
#%% raise
a=2
if a==1:
    print("ok")
else:
    raise Exception("値が1じゃない")
    


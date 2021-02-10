#mod2単体で動かす場合
#import mod1

#mod2がモジュールの場合
#from my_package import mod1
from . import mod1
#import my_package.mod1 #これはNG



from .sub_package1 import sub_mod1

def func_same():
    print('from mod2')
    mod1.func()


def func_sub():
    print('from mod2')
    sub_mod1.func()


if __name__ == '__main__':
    func_sub()
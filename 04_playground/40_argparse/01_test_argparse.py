# 1.import
import argparse

# 2. parserを作る
parser = argparse.ArgumentParser()

# 3. parser.add_argumentで受け取る引数を追加
parser.add_argument("arg1",help="これは入力です")
parser.add_argument("arg2")
parser.add_argument("--arg3") #オプション引数
parser.add_argument("-a","--arg4")

# 4. 引数を解析
args = parser.parse_args()

# 5. 引数の利用
print("arg1=" + args.arg1)
print("arg2=" + args.arg2)
print("arg3=" + args.arg3)
print("arg4=" + args.arg4)


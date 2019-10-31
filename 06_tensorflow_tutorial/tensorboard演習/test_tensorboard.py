# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:27:21 2019

@author: p000495138
"""

import tensorflow as tf

if __name__ == "__main__":

    sess = tf.InteractiveSession()

    # tensorboardログ出力ディレクトリ
    log_dir = ".\\log"

    # 計算グラフ定義
    a = tf.constant(1, name='a')
    b = tf.constant(2, name='b')
    op_add = tf.add(a , b)

    # このコマンドで`op_add`をグラフ上に出力
    tf.summary.scalar('op_add', op_add)

    # グラフを書く
    summary_writer = tf.summary.FileWriter(log_dir , sess.graph)

    # 実行
    sess.run(op_add)

    # SummaryWriterクローズ
    summary_writer.close()
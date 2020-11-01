
#!/usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------------------
# 色付きechoクラス
#------------------------------------------

import subprocess

# 色の定義クラス
class Color:
    BLACK          = '30'
    RED            = '31'
    GREEN          = '32'
    YELLOW         = '33'
    BLUE           = '34'
    WHITE          = '37'

# 色付きechoクラス
class Printer:
    # classmethod = static
    @classmethod
    def msg(self, msg, color=Color.WHITE, newLine=True):
        # pythonの三項演算子らしい
        # newLineがTrueなら、改行する
        msg = msg + '\n' if newLine else msg

        # エスケープシーケンスで色を付ける
        colored_msg = '\e[{}m{}\e[m'.format(color, msg)

        # -n = 改行なし
        # -e = エスケープシーケンスを解釈する
        subprocess.call(['echo', '-n', '-e', colored_msg])
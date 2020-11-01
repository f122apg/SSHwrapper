#!/usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------------------
# sys.argvのコントローラークラス
#------------------------------------------

import re

class ArgController:
    # IP形式 or FQDN or localhostを接続先として認識する
    REGEXP_CONNECT_TO = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\w+\.\w+|localhost)'

    def __init__(self, args):
        del args[0]
        self._args = args

    def get_ip(self):
        # 前から検索すると鍵ファイルなどがヒットする恐れがあるので、後ろから検索する
        args = self._args[::-1]
        for arg in args:
            matched = re.search(self.REGEXP_CONNECT_TO, arg)
            if matched:
                return matched.group(0)

    def get_args(self):
        return self._args
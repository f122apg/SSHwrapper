#!/usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------------------
# SSHコマンド実行クラス
#------------------------------------------

import subprocess

class Command:
    @classmethod
    def exec_ssh(self, args):
        params = args
        # command sshとするとエイリアスを無視できる
        params.insert(0, 'command')
        params.insert(1, 'ssh')

        subprocess.call(params)
#!/usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------
# SSHwrapper ver1.0
#
# sshで接続しようとしているIPアドレスの情報を表示し、適宜接続確認を行う
#-------------------------------------------------------------

import json
import sys
import subprocess
import os

from arg_controller import ArgController
from command import Command
from printer import Printer, Color

# 定数
# IPアドレスの情報を格納するjsonファイル
# このjsonを元に指定されたIPアドレスがどんな環境なのか調べる
CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__), '../config/ip_config.json'))
# ssh_confirm設定を無視してでも接続確認を行うレベル
CONNECT_CONFIRM_LEVEL = [ 'production' ]
# y/Nで使える文字列
# 基本的にここはいじらない
YN_LIST = {
    # yes
    'y': [
        'yes',
        'ye',
        'y',
    ],
    # no
    'n': [
        'no',
        'n',
        '' # 何も入力せずにEnterを押した際に反応する
    ]
}

# 最初のメッセージ
Printer.msg('-------------------- ssh wrapper --------------------')
Printer.msg('設定ファイルのパス:' + CONFIG_FILE)

# 引数からIPを取得する
arg_con = ArgController(sys.argv)
arg_ip = arg_con.get_ip()

Printer.msg('指定されたIPアドレス：' + str(arg_ip))
Printer.msg('-----------------------------------------------------')
Printer.msg('')

# 引数にIPっぽいのがなければ、そのまま実行
if arg_ip == None:
    Command.exec_ssh([])
    sys.exit(0)

# 設定ファイルがなければ、エラーで終える
if not os.path.isfile(CONFIG_FILE):
    Printer.msg('設定ファイルが存在しません。ファイルを作成してください。')
    sys.exit(1)

# SSH接続の前にメッセージを表示するか
is_notice = False
# SSH接続の前に接続確認をするか
is_need_confirm = False
# メッセージ出力のレベル
ip_level = 'development'

# jsonの読み込み
f = open(CONFIG_FILE, 'r')

try:
    ip_config = json.load(f)
except ValueError:
    Printer.msg('設定ファイルはjsonファイルではありません。')
    sys.exit(1)

for ip in ip_config:
    if arg_ip == ip['ip']:
        is_notice = True
        is_need_confirm = ip['ssh_confirm']
        ip_level = ip['level']
        env_name = ip['env_name']

        # レベルが一定以上であれば、ssh_confirmの設定は無視して必ず接続確認を行う
        if ip_level in CONNECT_CONFIRM_LEVEL:
            is_need_confirm = True
        break

# 設定ファイルと同一IPがあれば、メッセージを表示する
if is_notice:
    # 本番環境だけ警告文を表示
    if ip_level == 'production':
        Printer.msg('###########################################', Color.RED)
        Printer.msg('##############      警告      #############', Color.RED)
        Printer.msg('###########################################', Color.RED)

    Printer.msg('このIPアドレスは、「', newLine=False)
    Printer.msg(env_name, Color.GREEN, newLine=False)
    Printer.msg('」の',  newLine=False)

    # レベルごとに表示を変更
    if ip_level == 'production':
        Printer.msg('本番環境', Color.RED, newLine=False)
    elif ip_level == 'staging':
        Printer.msg('運用保守環境', Color.YELLOW, newLine=False)
    elif ip_level == 'development':
        Printer.msg('開発環境', Color.BLUE, newLine=False)

    Printer.msg('です。')
else:
    Printer.msg('このIPアドレスは設定ファイルに定義されていません！', Color.YELLOW)
    Printer.msg('直ちに定義してください！', Color.YELLOW)

# 設定ファイルと同一IPがあり、接続を確認するレベルのIPであれば、確認をとる
if is_need_confirm:
    Printer.msg('本当に接続しますか？', Color.YELLOW)

    # y/N/空が入力されるまで、ループ
    while True:
        try:
            choice = raw_input('[y/N] > ').lower()
        except (EOFError, KeyboardInterrupt): # EOFError = Ctrl+D, KeyboradInterrupt = Ctrl+C
            sys.exit(1)

        if choice in YN_LIST['n']:
            Printer.msg('SSH接続を中止しました。')
            sys.exit(0)
        elif choice in YN_LIST['y']:
            break

Printer.msg(arg_ip + ' へ接続します...')

try:
    Command.exec_ssh(arg_con.get_args())
except (EOFError, KeyboardInterrupt): # EOFError = Ctrl+D, KeyboradInterrupt = Ctrl+C
    sys.exit(1)
# SSHwrapper
  
SSHコマンドのラッパー。
  
SSH接続の前に、接続先の情報の表示や接続確認を行う。
  
# 必要要件
  - Python ver2.7
      - ver2.7.18で動作確認済み。
  - OpenSSH
      - SSHコマンドを使用するので。
  
# 使い方
  1. ```.bashrc```に以下の通り、記載する
  ```
  alias ssh='python ～/SSHWrapper/src/main.py'
  ```
  
# 設定ファイル
  
config/ip_config.jsonで接続先毎の情報を記載する。
  
設定サンプル
```
[
    {
        "ip": "127.0.0.1",
        "level": "production",
        "env_name": "sample",
        "ssh_confirm": "false"
    },
    {
        "ip": "localhost",
        "level": "development",
        "env_name": "me",
        "ssh_confirm": "true"
    }
]
```

 - ip
    - 接続先。FQDNでも可能。
 - level
    - 接続先のレベル。レベルによって警告文を表示する。用意されているレベルは以下の通り。
    1. production
         - 本番環境
    2. staging
         - 運用保守環境
    3. development
         - 開発環境
 - env_name
    - 接続先の環境名。
 - ssh_confirm
    - SSH接続する前に確認をとるか。```level```が```production```ならば、この設定は無視され、常に接続確認を行う。
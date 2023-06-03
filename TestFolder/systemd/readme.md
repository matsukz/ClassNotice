# systemdによる自動起動
systemdでClassNoticeをコントロールします。

## メインのPythonファイル
* ディレクトリ
  * `/opt`  
* 権限は0775
  * sudo chmod 0775 /opt/pythonfile.py
  * pipで外部モジュールを利用している場合は`sudo`でインストールし直す
  * `open()`でファイルを読み込むときはフルパスを記述する

## ClassNotice.service
* ディレクトリ
  * `/etc/systemd/system`
* 注意点
  * ファイル名がサービス名になる
  * `screen`などコンソールが必要なプログラムは起動不可
    * `print`で出力されるものがsystemdのログになる  
  * `sudo systemctl daemon-reload`を実行する

## ClassNotice.timer
* ディレクトリ
  * `/etc/systemd/system` 
* 注意点
  *  `sudo systemctl daemon-reload`を実行する

# 参考
* [pythonスクリプトをdaemonにする[systemd編] - Qiita](https://qiita.com/katsuNakajima/items/7ece6c74f992f652d732)

* [systemdで定期的にスクリプト実行 - ものものテック](https://monomonotech.jp/kurage/raspberrypi/systemd_timer.html)
* ChatGPT3.5

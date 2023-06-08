# 文字列操作
* `ClassNotice.py`で本日の授業一覧を出力するのに使いました。
* 2023-06-08に更新したVersion3以降の`Class.json`が必要です。
* ChatGPTしか使ってないから内容を残しておきます。
**出典不明で申し訳ないです。**

## ループでjsonの中身を取り出し出力
```Python
json_data = json.loads(data)

for item in json_data.values():
    print(item["name"])
```
`item`でループ回数を管理、ループ回数に対応したデータをjsonから引っ張ってくるらしい

## 文字列の操作
## 変数に文字列を追記
```Python
>>Data = "ハロー"
>>Data += "ワールド"

ハローワールド
```
## 変数へ改行を含めた文字列の格納
```Python
>>Data = "ハロー\nワールド"

ハロー
ワールド
```
```Python
>>Data = "ハロー\n"
>>Data += "ワールド"

ハロー
ワールド
```
## 最後尾の文字列を削除
```Python
>>Data = Data.rstrip("\n")
```
上記は改行コードだが普通の文字列でもいける

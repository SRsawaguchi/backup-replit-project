# backup-replit-project
個人用のスクリプトです。  

replitに作成したコードをgitにバックアップする。  
replit teamsを想定。  

projectのベースとなるrepositpryが存在する場合、利用可能。  

## スクリプトの仕組み
※あらかじめreplitからprojectのZIPをダウンロードしておく。  

以下のような手順を自動化するスクリプトです。  

1. ZIPを`./tmp`に展開する。  
2. 展開して出てきたファイルのうち、コマンドでしていしたパターンにマッチするファイルを削除する。  
3. 指定したリポジトリにZIPファイルのファイル名でブランチを作成
4. 展開したファイルをリポジトリにコピーする。
5. commit & push
6. ZIPで展開したファイルを全て削除し、スプリプと実行前のブランチをチェックアウトする。  

## オプション
- repo: リポジトリのパス
- zip: ZIPファイルのパス
- pattern 任意: ファイルの除外パターン。コンマで区切って複数指定できる。パターンにマッチするファイルはリポジトリにコピーされない。(例: `*.sqlite3,*.png,Makefile,README.md,schema.sql`)
- remote 任意: pushするリモートの名前。デフォルトは`origin`。

## 実行例

```
python3 backup_replit.py \
	--repo path_to_repo \
	--zip path_to_zip/replit_project.zip \
	--pattern 'bin/*' 
```

hint: `xargs`を使って一括処理する。  

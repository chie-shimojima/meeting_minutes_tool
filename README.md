# meeting_minutes_tool

録音データからAIで議事録を自動生成し、Google Docsへ保存するツールです。

## 使用技術

* Python
* OpenAI API
* Google Docs API
* OAuth認証

## 実装機能

* 音声ファイルの文字起こし
* AIによる議事録生成
* Google Docsへの自動保存
* URL自動出力

## 実行方法

```bash
pip install -r requirements.txt
python main.py
```

## 注意

`.env`、`credentials.json`、`token.json` はGitHubへ公開しないよう `.gitignore` に追加しています。

今後はZoom録音データや会議データとの連携も検討しています。

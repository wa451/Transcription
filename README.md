# 文字起こしツール（Whisper + moviepy）

## 概要

このPythonスクリプトは、OpenAIのWhisperモデルとmoviepyを使って、動画や音声ファイルから日本語の文字起こし（自動書き起こし）を行います。

- 動画ファイルから音声を抽出し、Whisperでテキスト化します。
- 音声ファイルも直接文字起こし可能です。
- サポートされていない拡張子の場合はエラーを表示します。

## 対応ファイル拡張子

- 動画: `.mkv`, `.mp4`, `.avi`, `.mov`, `.flv`, `.wmv`, `.webm`, `.mpg`, `.mpeg`, `.3gp`, `.ts`
- 音声: `.mp3`, `.wav`, `.m4a`, `.aac`, `.ogg`, `.wma`, `.aiff`, `.amr`, `.opus`

## 必要なライブラリ

- [openai-whisper](https://github.com/openai/whisper)
- [moviepy](https://github.com/Zulko/moviepy)

インストール例:

```
pip install openai-whisper moviepy
```

## 使い方

1. `input_file_path` 変数に処理したい動画または音声ファイルのフルパスを指定します。
    - 例: `input_file_path = "C:/Users/ユーザー名/Downloads/サンプル動画.mp4"`
2. スクリプトを実行します。

    ```
    python 文字起こし.py
    ```

3. 文字起こし結果は、スクリプトを実行したカレントディレクトリ直下の `output/output.txt` に保存されます。

## 注意事項

- Whisperモデルの初回利用時はモデルデータのダウンロードが必要です。
- 高精度な文字起こしには `base` 以上のモデル推奨（`small`, `medium`, `large` など）。
- ファイルパスや拡張子が正しいか必ず確認してください。
- サポート外の拡張子の場合はエラーが表示されます。


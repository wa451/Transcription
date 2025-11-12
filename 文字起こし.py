import whisper
import os
import moviepy as mp

def transcribe_with_whisper(audio_path, output_text_path="transcription_whisper.txt", model_name="small"):
    """
    Whisperモデルを使用して音声ファイルを文字起こしします。

    Args:
        audio_path (str): 入力音声ファイルのパス。
        output_text_path (str): 文字起こし結果のテキストファイルの出力パス。
        model_name (str): 使用するWhisperモデルのサイズ ('tiny', 'base', 'small', 'medium', 'large'など)。
            日本語の認識には 'base' 以上が推奨されます。
            'large-v2' や 'large-v3' が最も高精度ですが、ダウンロードサイズが大きく、処理も重くなります。
    """
    try:
        # モデルをロード (初回実行時にダウンロードされます)
        model = whisper.load_model(model_name)
        
        # 音声ファイルを文字起こし
        result = model.transcribe(audio_path, language="ja", fp16=False) # fp16=False はCPU利用時、メモリ使用量削減のため推奨

        transcribed_text = result["text"]

        print("文字起こしが完了しました。")
        
        # 結果をテキストファイルに保存
        with open(output_text_path, "w", encoding="utf-8") as f:
            f.write(transcribed_text)
        
        print(f"文字起こし結果が {output_text_path} に保存されました。")

    except Exception as e:
        print(f"Whisperによる文字起こし中にエラーが発生しました: {e}")
        

def validate_and_extract_audio(input_file_path, extracted_audio_path):
    """
    ファイルの存在・拡張子チェックと音声抽出を行う関数。
    Args:
        input_file_path (str): 入力ファイルのパス
        extracted_audio_path (str): 抽出音声ファイルのパス
    Returns:
        str or None: 音声ファイルのパス（失敗時None）
    """
    # 対応可能な拡張子一覧
    supported_exts = [
        ".mkv", ".mp4", ".avi", ".mov", ".flv", ".wmv", ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".wma", ".webm", ".mpg", ".mpeg", ".3gp", ".ts", ".aiff", ".amr", ".opus"
    ]
    # ファイルの拡張子を取得
    _, ext = os.path.splitext(input_file_path)
    ext = ext.lower()

    if ext not in supported_exts:
        print(f"エラー: 対応していないファイル拡張子です: {ext}")
        print(f"対応可能な拡張子: {', '.join(supported_exts)}")
        return None
    if not os.path.exists(input_file_path):
        print(f"エラー: 指定されたファイル '{input_file_path}' が見つかりません。")
        print("`input_file_path` をあなたのファイルへの正しいパスに設定してください。")
        print("または、テスト用の音声ファイルを用意して、直接 transcribe_with_whisper を呼び出してください。")
        return None

    # 音声ファイルならそのまま返す
    if ext in [".mp3", ".wav", ".m4a", ".aac", ".ogg", ".wma", ".aiff", ".amr", ".opus"]:
        print(f"音声ファイルを直接使用します: {input_file_path}")
        return input_file_path
    # 動画ファイルなら抽出
    print(f"動画ファイルから音声を抽出中: {input_file_path} -> {extracted_audio_path}")
    try:
        video = mp.VideoFileClip(input_file_path)
        audio = video.audio
        audio.write_audiofile(extracted_audio_path)
        audio.close()
        video.close()
        print("音声抽出が完了しました。")
        return extracted_audio_path
    except Exception as e:
        print(f"音声の抽出中にエラーが発生しました: {e}")
        return None

if __name__ == "__main__":
    input_file_path = f"" # 入力ファイルのパスを指定
    extracted_audio_path = "extracted_audio_for_whisper.wav"

    # カレントディレクトリからoutput/output.txtの絶対パスを生成
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, "output")
    output_text_path = os.path.join(output_dir, "output.txt")
    # outputディレクトリがなければ作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # ファイルの確認と音声抽出
    audio_path = validate_and_extract_audio(input_file_path, extracted_audio_path)

    # 文字起こし
    if audio_path and os.path.exists(audio_path):
        transcribe_with_whisper(audio_path, output_text_path, "small")

        # 一時音声ファイルを削除
        if audio_path != input_file_path and os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"一時音声ファイル {audio_path} を削除しました。")
    else:
        print("音声抽出に失敗したため、文字起こしをスキップします。")
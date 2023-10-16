from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# メモの内容を保存するファイルパス
text_file = 'text.txt'
# ログを保存するファイルパス
log_file = 'log.txt'

# ダークテーマのCSS
dark_theme_css = """
<style>
    body {
        background-color: #333;
        color: #fff;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }
    textarea {
        background-color: #444;
        color: #fff;
        width: 80%; /* ページの幅の80%を占める */
        height: 300px; /* 適切な高さを設定 */
        font-size:1.1rem;
        padding:30px;
    }
</style>
"""


@app.route('/')
def index():
  # ページを開いたとき、text.txtの内容を読み込んでテキストエリアに表示
  if os.path.exists(text_file):
    with open(text_file, 'r') as file:
      text = file.read()
  else:
    text = ''

  return render_template('index.html', text=text, css=dark_theme_css)


@app.route('/update', methods=['POST'])
def update_text():
  text = request.form.get('text', '')

  # テキストをリアルタイムにtext.txtに保存
  with open(text_file, 'w') as file:
    file.write(text)

  # ログを log.txt に追記
  with open(log_file, 'a') as file:
    file.write(text + '\n')

  return jsonify({'status': 'success'})


if __name__ == '__main__':
  app.run()

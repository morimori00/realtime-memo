from flask import Flask, render_template, request, jsonify
import datetime 
import json

app = Flask(__name__)

TEXT_FILE = 'text.txt'
LOG_FILE = 'log.json'

prev_text = ''

def load_text():
    with open(TEXT_FILE, 'r') as f:
        return f.read()

def save_text(text):
    with open(TEXT_FILE, 'w') as f:
        f.write(text)

def write_log(text):
    global prev_text

    diff = abs(len(text) - len(prev_text))
    if diff >= 30:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log = {'time': now, 'text': text}
        with open(LOG_FILE, 'r+') as f:
            logs = json.load(f) 
            logs.append(log)
            f.seek(0) 
            json.dump(logs, f)

    prev_text = text


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_text', methods=['POST'])
def update_text():
    data = request.get_json()
    text = data['text']

    save_text(text)
    write_log(text)

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run()
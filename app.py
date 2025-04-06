# app.py

import os
from flask import Flask, render_template, request, send_from_directory
from pydub import AudioSegment
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

SUPPORTED_FORMATS = {'.wav', '.flac', '.ape', '.alac', '.wv', '.mp3', '.aac', '.ogg', '.opus', '.webm', '.m4a'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "❌ 沒有選擇檔案"
    file = request.files['file']
    if file.filename == '':
        return "⚠️ 檔案名稱為空"

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        return f"❌ 不支援的音訊格式：{ext}"

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    if ext == '.mp3':
        return f"✅ 檔案已是 MP3：{filename}"

    output_filename = os.path.splitext(filename)[0] + ".mp3"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="mp3")
        return f"✅ 轉換完成：<a href='/download/{output_filename}' download>點我下載 MP3</a>"
    except Exception as e:
        return f"❌ 轉換錯誤：{e}"

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

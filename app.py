from flask import Flask, render_template, request, send_file
from docx import Document
from datetime import datetime
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    # Get the transcribed text from the client
    transcript_text = request.form.get('transcript_text', '')

    if not transcript_text.strip():
        return "Error: No text provided for download.", 400

    # Save the transcript to a Word document
    file_name = f"Transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    document = Document()
    document.add_paragraph(transcript_text)
    document.save(file_path)

    # Send the file for download
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

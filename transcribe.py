from flask import Flask, request, send_file, render_template, jsonify
import os
import whisper  # If using Whisper

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
TRANSCRIPT_FOLDER = 'transcripts'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_and_transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # Transcription process (using Whisper as an example)
        model = whisper.load_model("tiny")
        result = model.transcribe(file_path)
        transcript_text = result['text']

        # Save the transcript to a text file
        transcript_file_path = os.path.join(TRANSCRIPT_FOLDER, f"{file.filename}.txt")
        with open(transcript_file_path, 'w') as transcript_file:
            transcript_file.write(transcript_text)

        # Clean up the uploaded MP4 file
        os.remove(file_path)

        # Send back the transcript file
        return send_file(transcript_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

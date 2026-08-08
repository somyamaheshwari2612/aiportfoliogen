import os
from flask import Flask, render_template, request, jsonify, send_file
from config import Config
from services import generate_resume_portfolio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', themes=app.config['THEMES'])

@app.route('/generate', methods=['POST'])
def generate():
    if 'resume' not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400
        
    if not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Invalid file type. Allowed: .txt, .pdf, .docx"}), 400
        
    theme = request.form.get('theme', 'modern')
    if theme not in app.config['THEMES']:
        theme = 'modern'
        
    try:
        result = generate_resume_portfolio(file, theme)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/download/html', methods=['GET'])
def download_html():
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'portfolio.html')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name='portfolio.html')
    return "File not found", 404

@app.route('/download/pdf', methods=['GET'])
def download_pdf():
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'portfolio.pdf')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name='portfolio.pdf')
    return "PDF generation not yet implemented or file not found.", 404

if __name__ == '__main__':
    app.run(debug=True)

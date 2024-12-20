from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from markitdown import MarkItDown
import tempfile

markdown_convert = Blueprint('markdown_convert', __name__)

ALLOWED_EXTENSIONS = {
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 
    'ppt', 'pptx', 'txt', 'html'
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@markdown_convert.route('/markdown')
def index():
    return render_template('markdown_convert.html')

@markdown_convert.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'No file uploaded'
        })
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': 'No file selected'
        })
    
    if not allowed_file(file.filename):
        return jsonify({
            'status': 'error',
            'message': 'Unsupported file type'
        })
    
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            file.save(temp.name)
            md = MarkItDown()
            result = md.convert(temp.name)
            os.unlink(temp.name)
            
            return jsonify({
                'status': 'success',
                'content': result.text_content
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })
from flask import Flask
from flask import render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
import os
from PDFOps import PdfOps

app = Flask(__name__)

# uses environment variable if exists, else 'string'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
# path to uploaded files
app.config['UPLOAD_FOLDER'] = 'upload'
# max size of uploaded files
#app.config['MAX_CONTENT_PATH'] = 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/append', methods=['POST', 'GET'])
def append():
    paths = []
    if request.method == 'POST':
        for file in request.files.getlist('file'):
            # if user doesn't select file, browser submits empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            # save file if valid
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            paths.append(os.path.join('upload/', file.filename))
        # append uploaded files
        p = PdfOps(paths[0])
        p.append(paths[1:])
        # remove uploaded files
        for file in paths:
            os.remove(file)
    return render_template('ops.html', operation='Append')

@app.route('/output')
def output():
    return '''<!doctype html><h1>Show outputted files</h1>'''

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

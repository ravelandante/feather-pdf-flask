from flask import Flask
from flask import render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
import os
from PDFOps import PdfOps

app = Flask(__name__)
# path to uploaded files
app.config['UPLOAD_FOLDER'] = 'upload'
# max size of uploaded files
#app.config['MAX_CONTENT_PATH'] = 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in 'pdf'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user doesn't select file, browser submits empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # save file if valid
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('append'))

@app.route('/append')
def append():
    #paths = paths.split(',')
    paths = ['c.pdf', 'cl.pdf']
    p = PdfOps(paths[0])
    p.append(paths[1:])
    return render_template('append.html', operation='Append')

@app.route('/output')
def output():
    return '''<!doctype html><h1>Show outputted files</h1>'''

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

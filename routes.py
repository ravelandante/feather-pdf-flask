from flask import Flask
from PDFOps import PdfOps

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Light PDF</h1>'

@app.route('/append/<paths>')
def append(paths):
    paths = paths.split(',')
    p = PdfOps(paths[0])
    p.append(paths[1:])
    return 'Appended!'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

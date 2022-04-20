from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.utils import secure_filename,send_file

app=Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def success():
    global file
    if request.method=='POST':
        file=request.files['file']
        file.save(secure_filename('uploaded_' + file.filename))
        with open('uploaded_'+file.filename,'a+') as f:
            f.write('This was added to the file')
        return render_template('index.html', text='**file uploaded successfully**',btn='download.html')


@app.route('/download')
def download():
    return send_file('uploaded_'+file.filename, download_name="yourfile.csv", as_attachment=True, environ=request.environ)


if __name__ == '__main__':
    app.debug=True
    app.run()
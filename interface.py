from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = './media/user_input'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/interact', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        if file1.filename == '':
            flash('No selected file')
            return "No selected file"
        if file1 and allowed_file(file1.filename):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
            file1.save(path)
            return render_template('calibration.html')
        return '''
        file not allowed
        <a href="/interact">go back</a>
        '''
    return render_template('interact.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/calibration', methods=['GET','POST'])
def calibration():
    return render_template('calibration.html')


if __name__ == '__main__':
    app.run()
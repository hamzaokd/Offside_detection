from re import U
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import os ,sys
import time
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from offside_detection import *
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image


UPLOAD_FOLDER = 'flask_app/static/user_input'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    
    return '''<html>
    <body>
    offside detection
    </body
    </html
    '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/interact.html', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file in form!'
        file1 = request.files['file1']
        if file1.filename == '':
            flash('No selected file')
            print("no")
            return "No selected file"
        if file1 and allowed_file(file1.filename):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
            # filename, file_extension = os.path.splitext(path)
            # name="user_image"+file_extension

            # npath=os.path.join(app.config['UPLOAD_FOLDER'], name)
            file1.save(path)
            file_name = file1.filename
            #convert to jpg
            im = Image.open(path)
            rgb_im = im.convert("RGB")
            npath=os.path.join(app.config['UPLOAD_FOLDER'], "user_image.jpg")
            rgb_im.save(npath)
            time.sleep(5)
            print(npath)
            
            
            return redirect('calibration.html')
        return '''
        file not allowed
        <a href="/interact">go back</a>
        '''
    return render_template('interact.html')



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

coord=[]
f,u=None,None
@app.route("/calibration.html", methods=["GET", "POST"])
def cali():
    global coord
    if request.method == "POST":
        field_coord = request.form["field_coord"]
        user_coord = request.form["user_coord"]
        req = request.form

        missing = list()

        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("calibration.html", feedback=feedback)
        
        coord=get_coord(field_coord, user_coord)
        return redirect("offside.html")
    return render_template("calibration.html")

# def get_coor(field,user):
#     global f,u
#     f=field
#     u=user
def get_coord(f, u):
    f_coord = f.split(",")
    u_coord = u.split(",")
    f_coord=np.float32([int(i) for i in f_coord]).reshape(4,2)
    u_coord=np.float32([int(i) for i in u_coord]).reshape(4,2)

    return f_coord, u_coord

@app.route("/offside.html", methods=["GET", "POST"])
def offside():
    global coord
    print("cord",coord)
    #coor=get_coord(coord[0], coord[1])
    M,U_w,U_sim=get_positions(coord)
    calibrate(M,U_w)
    return "done"

if __name__ == '__main__':
    app.run()
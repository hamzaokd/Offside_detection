"""
flask app
author:Hamza Oukaddi
"""

from re import U
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, session
from werkzeug.utils import secure_filename
import os ,sys
import time
import numpy as np
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from identification import get_field_positions
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired
from PIL import Image
import offs
import base64


UPLOAD_FOLDER = 'static\\user_input'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#csrf key
app.config['SECRET_KEY'] = 'secret'


# wtf form for the user to input the image
class Image_upload(FlaskForm):
    image = FileField('image', validators=[DataRequired()])
    submit = SubmitField('Upload')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    
    return render_template('about.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/auto')
def auto():
    return """
    Still not implemented, please use the interactive method <a href="interact.html">here</a> or go to the <a href="index.html">home page</a>
    """

@app.route('/interact.html', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
    # if form.validate_on_submit():
        uploaded_image = request.files['uploaded-file']

        # if uploaded_image.filename == '':
        #     flash('No selected file')
        #     print("no")
        #     return "No selected file"
        # if uploaded_image and allowed_file(uploaded_image.filename):
        img_filename = secure_filename(uploaded_image.filename)
        uploaded_image.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        img_file_path = session.get('uploaded_img_file_path', None)
        return redirect(url_for('cali'))
        return render_template('calibration.html', image_b64=img_file_path)
            
    
    return render_template('interact.html')



@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)
    # Display image in Flask application web page
    return render_template('show_image.html', user_image = img_file_path)
 

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

coord=[]
f,u=None,None
@app.route("/calibration.html", methods=["GET", "POST"])
def cali():
    global coord
    image_b64 = session.get('uploaded_img_file_path', None)
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
    return render_template("calibration.html", image_b64=image_b64)

def get_coord(f, u):
    f_coord = f.split(",")
    u_coord = u.split(",")
    f_coord=np.float32([int(i) for i in f_coord]).reshape(4,2)
    u_coord=np.float32([int(i) for i in u_coord]).reshape(4,2)

    return f_coord, u_coord

@app.route("/offside.html", methods=["GET", "POST"])
def offside():
    global coord
    image_b64 = session.get('uploaded_img_file_path', None)
    print(image_b64, flush=True)
    # get_field_positions("flask_app/static/user_input/user_image.jpg") #imported from identification.py
    detected_players = get_field_positions(image_b64,image_b64) #imported from identification.py
    if detected_players is None:
        return render_template("no_player.html")
    detected_players_path = image_b64.replace(".","_detected.")
    offs.get_offsides(coord,detected_players, image_b64)
    players_positions_path = image_b64.replace(".","_top_map.")
    offside_lines = image_b64.replace(".","_lines.")
    
    return render_template("offside.html",
                           f_coord=coord,
                           detected_players= detected_players_path,
                           players_positions=players_positions_path,
                           image_b64=image_b64,
                           offside_lines=offside_lines
                           )








@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
    
    
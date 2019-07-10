import os
import numpy as np
import pandas as pd
from PIL import Image
import urllib.request
import time
import tensorflow as tf
import tensorflow.contrib.eager as tfe

# import transfer_tools
from transfer_tools import run_style_transfer

from clean_up_gallery import (
    cleaning,
    pull_files
)

from gif_generator import(
    gif_generator
)

import json


from flask import (
    Flask,
    flash,
    redirect,
    url_for,
    session,
    render_template,
    send_from_directory,
    jsonify,
    request)

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# read in csv
art_df = pd.read_csv('static/csv/artist_and_art_titles.csv')

# enable eager execution
tf.enable_eager_execution()
print("Eager execution: {}".format(tf.executing_eagerly()))


#################################################
# Flask Routes
#################################################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/",  methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
    
        cleaning() #clean gallery and uploads
        print(request)

        data = request.form['quality'] #get iterations
        final_img_name = request.form['final_image_input'] #get unique file name

        if request.form['style-library-selected']: #if style from library
            style2 = request.form['style-library-selected']
            artist = style2.split("/")[4]
            title = (style2.split("/")[5]).split(".")[0]
            name = f'{artist}_{title}'
            save_image = os.path.join("static/uploads", f'{name}.jpg') #save image
            urllib.request.urlretrieve(style2, save_image) #save the image from the url

        if request.files.get('style'): #if style uploaded
            file = request.files['style']
            print(file)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if request.files.get('content'): #get content
            file = request.files['content']
            print(file)
            contentfilename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], contentfilename))

            content_path = f'static/uploads/{contentfilename}'
            try:
                style_path = f'static/uploads/{filename}'
            except:
                style_path = f'static/uploads/{name}.jpg'
            version = "none"
            
            imgs, best, best_loss = run_style_transfer(content_path, style_path, num_iterations=int(data))
            
            for i,img in enumerate(imgs): # save iterations
                actual_img = Image.fromarray(img)
                file_name = 'static/12-iterations/nst'+str(i)+'.png'
                actual_img.save(file_name)
            
            actual_img = Image.fromarray(best) #save images
            file_name_result = 'static/result/best.png'
            file_name_gallery = f'static/gallery/{final_img_name}.png'
            actual_img.save(file_name_result)
            actual_img.save(file_name_gallery)
            
            gif_generator() # generate the newest gif
        
            return render_template("form.html", contentfilename=(f'static/uploads/{contentfilename}'), filename=style_path, quality=data, version = version, best=file_name_gallery)
            
    return render_template("form.html")
@app.route("/gallery_images")
def gallery_images():
    gallery_imgs = pull_files()
    return jsonify(gallery_imgs)

@app.route("/art_data")
def data():
    art_data = {
        "art_image": art_df.Art_Piece.values.tolist(),
        "art_title": art_df.Piece_Title.values.tolist(),
        "artist": art_df.Artists.values.tolist()
        }
    return jsonify(art_data)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

@app.route('/result')
def result():
    return render_template("result.html") 

if __name__ == "__main__":
    app.run(debug=True)


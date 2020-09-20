import os
import cv2
import  sys
import numpy as np
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template
UPLOAD_FOLDER = 'uploads/'
SKETCH_FOLDER = 'sketch/'
COLOR_FOLDER = 'color/'
OIL_FOLDER = 'oil/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SKETCH_FOLDER'] = SKETCH_FOLDER
app.config['COLOR_FOLDER'] = COLOR_FOLDER
app.config['OIl_FOLDER'] = OIL_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        elif file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("saved file successfully")
      #send file name as parameter to downlad
            return redirect('/downloadfile/'+ filename)
    return render_template('upload.html')

@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)

@app.route('/sketch/<filename>')
def process(filename):
    file_path = UPLOAD_FOLDER + filename
    images = cv2.imread(file_path)
    image = cv2.resize(images, (960, 540))
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayImageInv = 255 - grayImage
    grayImageInv = cv2.GaussianBlur(grayImageInv, (25, 25), 0)
    output = cv2.divide(grayImage, 255 - grayImageInv, scale=256.0)
    cv2.imwrite('./sketch/' + filename, output)
    file_path1 = SKETCH_FOLDER + filename
    name="sketcherPencil_"+filename
    response=send_file(file_path1, mimetype='image/jpeg',as_attachment=True, attachment_filename=name)
    response.headers["x-filename"] = name
    response.headers["Access-Control-Expose-Headers"] = 'x-filename'
    return response

@app.route('/color/<filename>')
def process1(filename):
    file_path = UPLOAD_FOLDER + filename
    images = cv2.imread(file_path)
    image1 = np.array(images)
    image = cv2.resize(image1, (960, 540))
    sketch_gray, sketch_color = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    cv2.imwrite('./color/' + filename, sketch_color)
    file_path1 = COLOR_FOLDER + filename
    name1 = 'sketcherColor_' + filename
    response1=send_file(file_path1, mimetype='image/jpeg',as_attachment=True, attachment_filename=name1)
    response1.headers["x-filename"] = name1
    response1.headers["Access-Control-Expose-Headers"] = 'x-filename'
    return response1

@app.route('/oil/<filename>')
def process2(filename):
    file_path = UPLOAD_FOLDER + filename
    images = cv2.imread(file_path)
    image = cv2.resize(images, (960, 540))
    stylize = cv2.stylization(image, sigma_s=60, sigma_r=0.07)
    cv2.imwrite('./oil/' + filename, stylize)
    file_path1 = OIL_FOLDER + filename
    name2='sketcherOil_' + filename
    response2=send_file(file_path1,  mimetype='image/jpeg', as_attachment=True, attachment_filename=name2)
    response2.headers["x-filename"] = name2
    response2.headers["Access-Control-Expose-Headers"] = 'x-filename'
    return response2

if __name__ == "__main__":
    app.run()
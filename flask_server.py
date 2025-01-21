from flask import Flask, request, render_template, send_from_directory
from BM3D import bm3d_algorithm
import os

# app initialization
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('index.html')


# function to display the bm3d.html page
@app.route('/bm3d')
def bm3d():
    return render_template('bm3d.html')


# function to display the home.html page when the user presses the Home button on the navbar
@app.route('/index')
def home():
    return render_template('home.html')


@app.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


# function to get the final image path after being denoised
@app.route('/results/<path:filename>')
def get_denoised_image(filename):
    return send_from_directory('static', filename)


# function to run the bm3d denoise algorithm which will also post the image to the server
@app.route('/denoise', methods=['POST'])
def denoise():
    file = request.files['file']
    filename = file.filename
    filepath = os.path.join('uploads', filename)
    file.save(filepath)
    processed_image = bm3d_algorithm(filepath, filename)
    return processed_image


# main function
if __name__ == '__main__':
    app.run(debug=True)

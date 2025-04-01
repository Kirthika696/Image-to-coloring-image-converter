import cv2
import numpy as np
from flask import Flask, request, render_template, send_file
import os
import webbrowser
import threading

def convert_to_coloring_image(image_path, output_path='static/coloring_image.png'):
    # Load image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 10)
    
    # Save output image
    cv2.imwrite(output_path, edges)
    return output_path

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h2>image to coloring image generator</h2>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Upload">
                
            </form>
        </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], "input_image.png")
    file.save(input_path)
    output_path = convert_to_coloring_image(input_path)
    
    return f'''
    <h3>Coloring Image Generated</h3>
    <br>
    <img src="/{output_path}" width="400px">
    <br><br>
    <a href="/{output_path}" download>
        <button>Download Image</button>
    </a>
    <br><br>
    <a href="/">Upload Another Image</a>
    '''
    

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
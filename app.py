
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import cv2
from PIL import Image
import io

app = Flask(__name__)

# Function to simulate cross-domain colorization
def cross_domain_colorization(image, color_choice):
    # Convert the image to a numpy array
    img_array = np.array(image)

    # Simple colorization based on the chosen color
    if color_choice == 'red':
        img_array[..., 0] = 255  # Red channel
    elif color_choice == 'green':
        img_array[..., 1] = 255  # Green channel
    elif color_choice == 'blue':
        img_array[..., 2] = 255  # Blue channel

    return Image.fromarray(img_array)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    # Read the image file
    image = Image.open(file.stream).convert("RGB")
    
    # Get color choice from form
    color_choice = request.form['color_choice']
    
    # Perform colorization
    colorized_image = cross_domain_colorization(image, color_choice)
    
    # Save the colorized image to a bytes buffer
    img_byte_arr = io.BytesIO()
    colorized_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return redirect(url_for('index', filename='colorized_image.png'))

if __name__ == '__main__':
    app.run(debug=True)

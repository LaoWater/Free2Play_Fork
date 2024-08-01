from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
from test import image_blueprint, StationsMetrics  # Import your existing functions
from graph_main import generate_plot  # Assuming this is your plot generation function
import io
import sys

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/food_prophet')
def food_prophet():
    return render_template('the_food_prophet.html')

@app.route('/plot', methods=['POST'])
def plot():
    # Retrieve user input from the form
    user_input = {
        "Initial_KS2_Karmic_Balance": float(request.form.get("initial_ks2_balance", 0)),
        "Quality": float(request.form.get("quality", 0)),
        "Timing": float(request.form.get("timing", 0)),
        "Logistics": float(request.form.get("logistics", 0)),
        "Quantity": float(request.form.get("quantity", 1)),
    }

    # Generate the plot
    img = generate_plot(user_input)

    # Save the plot to the static directory
    plot_path = os.path.join('static', 'plot.png')
    with open(plot_path, 'wb') as f:
        f.write(img.read())

    # Render the plot.html template with the image URL
    return render_template('plot.html', plot_image='/static/plot.png')

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            stations_metrics = StationsMetrics()

            # Capture the script's printed output
            captured_output = io.StringIO()
            sys.stdout = captured_output
            blueprint_image = image_blueprint(file_path, stations_metrics)
            sys.stdout = sys.__stdout__
            script_output = captured_output.getvalue()

            processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + filename)
            cv2.imwrite(processed_image_path, blueprint_image)

            return render_template('uploaded_file.html', filename='processed_' + filename, script_output=script_output)
    return render_template('upload_image.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

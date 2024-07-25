from flask import Flask, render_template, request
from graph_main import generate_plot
import os

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
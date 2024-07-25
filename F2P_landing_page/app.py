from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def landing_page():
    return render_template('index.html')

@app.route('/food_prophet')
def food_prophet():
    return "<h1>You have been redirected to the food prophet</h1>"

if __name__ == '__main__':
    app.run(debug=True)
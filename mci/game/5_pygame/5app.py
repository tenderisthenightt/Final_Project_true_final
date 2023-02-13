from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def memory():
    return render_template('5index.html')

if __name__ == '__5main__':
    app.run(debug=True)
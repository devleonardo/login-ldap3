from flask import Flask, render_template

app = Flask(__name__)

@app.route('/base')
def base():
    return render_template('base.html')

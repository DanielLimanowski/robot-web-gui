from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')
0

if __name__ == '__main__':
    app.run()

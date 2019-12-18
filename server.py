from flask import Flask
from flask import render_template

from flask.cli import FlaskGroup

app = Flask(__name__)
cli = FlaskGroup(app)


@app.route('/', methods=['GET'])
def root():
    link = "https://vk.com/vitaliyrakitin"
    return render_template('index.html', link=link)


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=9084, threaded=True)
    cli()

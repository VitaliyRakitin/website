from flask import Flask
from flask import render_template
from flask.cli import FlaskGroup

app = Flask(__name__)
cli = FlaskGroup(app)


@app.route('/', methods=['GET'])
def root():
    print("In root")
    link = "https://vk.com/vitaliyrakitin"
    text = "Заходите в гости"
    return render_template('index.html', link=link, text=text)


@app.route('/google', methods=['GET'])
def google():
    print("In hay")
    link = "https://google.com/"
    text = "Заходите в гугл"
    return render_template('index.html', link=link, text=text)


if __name__ == '__main__':
    cli()

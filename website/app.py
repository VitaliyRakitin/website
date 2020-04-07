from flask import Flask, request, jsonify
from flask import render_template, Response
from flask.cli import FlaskGroup
from log import logger
from requests import post
# from flask_cors import CORS

app = Flask(__name__)
cli = FlaskGroup(app)
SECRET_KEY = ""


@app.route('/', methods=['GET'])
def root():
    link = "https://vk.com/vitaliyrakitin"
    text = "Заходите в гости"
    return render_template('index.html', link=link, text=text)


@app.route('/proxy', methods=['POST'])
def proxy_post():
    logger.info("PROXY POST: {0}".format(request.args))
    key = request.args.get('key')
    if key != SECRET_KEY:
        return jsonify({"status": False})

    url = request.args.get('url')
    result = post(url, request.data, request.headers).json()
    logger.info("PROXY result: {0}".format(result))
    return jsonify(result)


if __name__ == '__main__':
    cli()

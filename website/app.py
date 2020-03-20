from flask import Flask, request, jsonify
from flask import render_template
from flask.cli import FlaskGroup
from log import logger
from ya import find_ticket
app = Flask(__name__)
cli = FlaskGroup(app)
SECRET_KEY = ""

@app.route('/', methods=['GET'])
def root():
    link = "https://vk.com/vitaliyrakitin"
    text = "Заходите в гости"
    return render_template('index.html', link=link, text=text)


@app.route('/google', methods=['GET'])
def google():
    link = "https://google.com/"
    text = "Заходите в гугл"
    return render_template('index.html', link=link, text=text)


@app.route('/yandex_rasp', methods=['GET'])
def yandex_rasp():
    logger.info("GET YANDEX: {0}".format(request.args))
    key = request.args.get('key')
    if key != SECRET_KEY:
        return jsonify({"status": False})

    from_station = request.args.get('from')
    to_station = request.args.get('to')
    date = request.args.get('date')
    amount = request.args.get('amount')
    result = find_ticket(from_station, to_station, date, amount)
    logger.info("RESULT: {0}".format(result))
    return jsonify(result)


if __name__ == '__main__':
    cli()

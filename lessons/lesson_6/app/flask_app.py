from flask import Flask, request, jsonify

from lessons.lesson_6.app.card_model import Card
from lessons.lesson_6.app.card_repository import CardRepository

app = Flask(__name__)
card_repository = CardRepository('postgres')


@app.route('/', methods=['GET'])
def welcome():
    return 'Lesson 8 homework'


@app.route('/cards/<card_id>', methods=['GET'])
def get_card(card_id):
    return jsonify(card_repository.get_card(card_id=card_id).__dict__)


@app.route('/cards', methods=['POST'])
def create_card():
    request_json = request.json
    card_id = card_repository.save_card(
        Card(
            pan=request_json.get('pan'),
            cvv=request_json.get('cvv'),
            expiry_date=request_json.get('expiry_date'),
            issue_date=request_json.get('issue_date'),
            owner_id=request_json.get('owner_id'),
            status=request_json.get('status')
        )
    )
    return jsonify({'id': card_id})


if __name__ == "__main__":
    app.run(debug=True, port=8000)

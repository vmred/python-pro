from flask import Flask

from lessons.lesson_6.app.card_repository import CardRepository
app = Flask(__name__)
card_repository = CardRepository('postgres')


@app.route('/', methods=['GET'])
def welcome():
    return 'Lesson 8 homework'


@app.route('/cards/<card_id>', methods=['GET'])
def get_card(card_id):
    return card_repository.get_card(card_id=card_id).__dict__


if __name__ == "__main__":
    app.run(debug=True, port=8000)

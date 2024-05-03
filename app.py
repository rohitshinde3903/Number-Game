from flask import Flask, render_template, request, redirect, session, url_for
import random

app = Flask(__name__)

def initialize_game():
    return {
        'computer': random.randint(1, 100),
        'counter': 0,
        'guessed_numbers': []
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'game' not in session:
        session['game'] = initialize_game()

    game = session['game']

    message = ""
    result = False
    retain_focus = False  # Flag to retain focus on input field
    if request.method == 'POST':
        guess = int(request.form['guess'])
        game['counter'] += 1
        game['guessed_numbers'].append(guess)

        if guess != game['computer']:
            if guess > game['computer']:
                message = "Guess lower"
            else:
                message = "Guess higher"
            retain_focus = True  # Set the flag to retain focus on input field
        else:
            message = "Correct guess! You guessed it in {} attempts.".format(game['counter'])
            result = True

    return render_template('index.html', message=message, result=result, counter=game['counter'],
                           guessed_numbers=game['guessed_numbers'], retain_focus=retain_focus)

@app.route('/reset')
def reset():
    session.pop('game', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key='1'
    app.run(debug=True)

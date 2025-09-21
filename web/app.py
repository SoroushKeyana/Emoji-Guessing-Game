import csv
import random
from flask import Flask, render_template, request, session, redirect, url_for
from Levenshtein import ratio
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'emoji-guess-secret')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

CATEGORIES = ['Movies', 'TV Shows', 'Books', 'Video Games']
DIFFICULTY_LEVELS = ['Easy', 'Hard']
ROUNDS = 5

def load_puzzles(category, difficulty):
    items = []
    # Get absolute path to data.csv
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data.csv')
    data_path = os.path.abspath(data_path)
    with open(data_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Category'] == category and row['Difficulty'] == difficulty:
                items.append(row)
    return items

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        category = request.form.get('category')
        difficulty = request.form.get('difficulty')
        if category and difficulty:
            session['category'] = category
            session['difficulty'] = difficulty
            session['score'] = 0
            session['round'] = 0
            session['used_emojis'] = []
            session['hint_used'] = False
            session['matching_items'] = load_puzzles(category, difficulty)
            session['attempts'] = 0
            return redirect(url_for('game'))
    return render_template('index.html', categories=CATEGORIES, difficulties=DIFFICULTY_LEVELS)

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'matching_items' not in session or session['round'] >= ROUNDS:
        return redirect(url_for('score'))
    status = ''
    hint = ''
    attempts_left = 3 - session.get('attempts', 0)
    # Only get next item if new round
    if request.method == 'POST':
        answer = request.form.get('answer', '').strip().lower()
        current_item = session['current_item']
        correct = current_item['Title'].lower()
        if answer == 'hint':
            hint = current_item['Hint']
            session['hint_used'] = True
        elif answer == 'pass':
            status = f'Passed! The answer was: {current_item["Title"]}'
            session['round'] += 1
            session['hint_used'] = False
            session['attempts'] = 0
            # Get next item for new round
            available = [item for item in session['matching_items'] if item not in session['used_emojis']]
            if not available:
                return redirect(url_for('score'))
            item = random.choice(available)
            session['used_emojis'].append(item)
            session['current_item'] = item
            attempts_left = 3
            return render_template('game.html', round=session['round']+1, emoji=item['Emojis'], status=status, hint=hint, attempts_left=attempts_left)
        else:
            similarity = ratio(answer, correct)
            if similarity > 0.8:
                if session.get('hint_used', False):
                    session['score'] += 0.5
                else:
                    session['score'] += 1
                status = f'Correct! The answer was: {current_item["Title"]}'
                session['round'] += 1
                session['hint_used'] = False
                session['attempts'] = 0
                # Get next item for new round
                available = [item for item in session['matching_items'] if item not in session['used_emojis']]
                if not available:
                    return redirect(url_for('score'))
                item = random.choice(available)
                session['used_emojis'].append(item)
                session['current_item'] = item
                attempts_left = 3
                return render_template('game.html', round=session['round']+1, emoji=item['Emojis'], status=status, hint=hint, attempts_left=attempts_left)
            else:
                session['attempts'] = session.get('attempts', 0) + 1
                attempts_left = 3 - session['attempts']
                if session['attempts'] >= 3:
                    status = f"💥 You've used all your attempts. The correct answer was: {current_item['Title']}"
                    session['round'] += 1
                    session['hint_used'] = False
                    session['attempts'] = 0
                    # Get next item for new round
                    available = [item for item in session['matching_items'] if item not in session['used_emojis']]
                    if not available:
                        return redirect(url_for('score'))
                    item = random.choice(available)
                    session['used_emojis'].append(item)
                    session['current_item'] = item
                    attempts_left = 3
                    return render_template('game.html', round=session['round']+1, emoji=item['Emojis'], status=status, hint=hint, attempts_left=attempts_left)
                else:
                    status = f'Wrong! Try again. Attempts left: {attempts_left}'
    # If GET or wrong answer, show current emoji
    item = session['current_item']
    return render_template('game.html', round=session['round']+1, emoji=item['Emojis'], status=status, hint=hint, attempts_left=attempts_left)

@app.route('/score')
def score():
    score = session.get('score', 0)
    msg = f'Game Over! Your score is {score}.'
    if score >= 5:
        msg += "<br>Incredible! You're a master!"
    elif score >= 4:
        msg += "<br>Great job! You're doing awesome!"
    elif score >= 3:
        msg += "<br>Not bad, but there's room for improvement!"
    else:
        msg += "<br>Keep practicing! You'll get there!"
    return render_template('score.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)

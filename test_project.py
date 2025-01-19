from unittest.mock import patch
from io import StringIO
from project import get_user_selection, get_user_preferences, game_rounds


data = [
    {'Title': 'Inception', 'Emojis': '🌀💭', 'Hint': 'A mind-bending movie', 'Category': 'Movies', 'Difficulty': 'Easy'},
    {'Title': 'Stranger Things', 'Emojis': '🧑‍🤝‍🧑💀', 'Hint': 'A Netflix series', 'Category': 'TV Shows', 'Difficulty': 'Easy'},
    {'Title': 'Titanic', 'Emojis': '🚢💔', 'Hint': 'A tragic love story', 'Category': 'Movies', 'Difficulty': 'Medium'},
    {'Title': 'Breaking Bad', 'Emojis': '🧑‍🔬💊', 'Hint': 'A story about chemistry', 'Category': 'TV Shows', 'Difficulty': 'Hard'},
    {'Title': 'Avatar', 'Emojis': '🌍💫', 'Hint': 'A movie set on a distant planet', 'Category': 'Movies', 'Difficulty': 'Easy'}
]


def test_game_rounds_correct_guess(capsys):
    with patch('builtins.input', side_effect=['inception', 'stranger things', 'titanic', 'breaking bad', 'avatar',]), \
         patch('random.choice', side_effect=[data[0], data[1], data[2], data[3], data[4]]):
         score = game_rounds(data)

    captured = capsys.readouterr()

    assert score == 5
    assert '✅ You got it right!' in captured.out
    assert '❌ Wrong, Try again' not in captured.out


def test_game_rounds_incorrect_guess(capsys):
    with patch('builtins.input', side_effect=[
        'w', 'w', 'w',
        'stranger things',
        'w','titanic',
        'w', 'w', 'w',
        'w', 'avatar',]), \
         patch('random.choice', side_effect=[data[0], data[1], data[2], data[3], data[4]]):
         score = game_rounds(data)

    captured = capsys.readouterr()

    assert score == 3
    assert '✅ You got it right!' in captured.out
    assert '❌ Wrong, Try again' in captured.out


def test_game_rounds_hint_pass(capsys):
    with patch('builtins.input', side_effect=[
        'hint', 'avatar', 'inception',
        'stranger things',
        'hint', 'w','titanic',
        'hint', 'w', 'w', 'w',
        'pass',]), \
         patch('random.choice', side_effect=[data[0], data[1], data[2], data[3], data[4]]):
         score = game_rounds(data)

    captured = capsys.readouterr()

    assert score == 2
    assert '✅ You got it right!' in captured.out
    assert '❌ Wrong, Try again' in captured.out
    assert '🗝️  A mind-bending movie 🗝️' in captured.out
    assert '🗝️  A tragic love story 🗝️' in captured.out
    assert '🗝️  A story about chemistry 🗝️' in captured.out
    assert '❌ Question passed.' in captured.out


def test_get_user_selection_valid():
    options = {'1': 'Movies', '2': 'TV-Shows', '3': 'Books'}
    prompt = 'category'

    with patch('builtins.input', side_effect=['2']), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:

        assert get_user_selection(options, prompt) == 'TV-Shows'
        assert 'Select a category' in mock_stdout.getvalue()
        assert '1. Movies' in mock_stdout.getvalue()
        assert '2. TV-Shows' in mock_stdout.getvalue()
        assert '3. Books' in mock_stdout.getvalue()


def test_get_user_selection_invalid():
    options = {'1': 'Movies', '2': 'TV-Shows', '3': 'Books'}
    prompt = 'category'

    with patch('builtins.input', side_effect=['10', '15', '2']), \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:

        assert get_user_selection(options, prompt) == 'TV-Shows'
        assert 'Invalid selection. Please try again.' in mock_stdout.getvalue()
        assert mock_stdout.getvalue().count('1. Movies') == 3


def test_get_user_preferences_valid():
    with patch('builtins.input', side_effect=['2', '1']), \
         patch('project.generate_puzzle') as mock_generate_puzzle, \
         patch('project.clear_terminal') as mock_clear_terminal:

        get_user_preferences()

        mock_generate_puzzle.assert_called_once_with('TV Shows', 'Easy')
        assert mock_clear_terminal.call_count == 3


def test_get_user_preferences_invalid():
    with patch('builtins.input', side_effect=['10', '3', '5', '4', '1']), \
         patch('project.clear_terminal') as mock_clear_terminal, \
         patch('project.generate_puzzle') as mock_generate_puzzle, \
         patch('sys.stdout', new_callable=StringIO) as mock_stdout:

        get_user_preferences()

        assert 'Invalid selection. Please try again.' in mock_stdout.getvalue()
        mock_generate_puzzle.assert_called_once_with('Books', 'Easy')
        assert mock_clear_terminal.call_count == 6

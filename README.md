# Emoji Guessing Game
#### Video Demo: https://youtu.be/9LgNJ5E5_To
#### Description:
Emoji Guessing Game is a terminal-based game that players can pick a category and difficulty level and then they will be shown to guess the title of a movie, TV-show, book or video-game based on a set of emojis shown to them. The game has several categories and two difficulty levels. User's have the ability to get a hint or pass the round. The score will be calculated and shown to the user at the end.

- Multiple categories such as Movies, TV Shows, Books, and Video Games.
- Two difficulty levels: Easy and Hard.
- A scoring system that rewards correct answers and deducts points for hints.

#### Features:
- **Interactive Gameplay**: Players can choose from different categories and difficulty levels. Then the players are guided through five rounds of emoji puzzles.
- **Hint System**: Players can request hints bt typing 'hint' but will receive fewer points.
- **Pass**: Players can pass a round by typing 'pass' if they feel like they will never get the correct answer.
- **Content**: Questions are sourced dynamically from a CSV file.
- **Non-repeated**: Questions are randomized but it is ensured to not show a repeated question to the user.
- **Colorama**: Making the terminal colorful for better user experience.

#### Project Structure:
- **`project.py`**: Contains the main logic of the game. It contains 9 functions including main.
- **`data.csv`**: Stores the game data (Title, Emojis, Category, Difficulty, Hint).
- **`test_project.py`**: Includes tests to validate key functions such as `get_user_selection`, `get_user_preferences` and `game_rounds` using `pytest`.
- **`requirements.txt`**: Lists all external libraries such as `colorama` and `Levenshtein`.

#### Functions Overview
Here are the functions in the project and what they do:

- **`main()`**: The entry point of the game. Initializes the game, displays the welcome message, and handles errors like missing files.
- **`welcome_message()`**: Prints the game’s welcome screen and rules.
- **`clear_terminal()`**: Clears the terminal screen for a cleaner user experience.
- **`get_user_selection(options, prompt)`**: Prompts the user to select a category or difficulty level and validates their input.
- **`get_user_preferences()`**: Collects user preferences (category and difficulty) and starts the game.
- **`generate_puzzle(category, difficulty)`**: Gets the puzzles from `data.csv` based on user preferences and starts the game rounds.
- **`print_puzzle_intro()`**: Displays an introduction to the puzzle round.
- **`game_rounds(matching_items)`**: Handles the core gameplay, including presenting questions, managing attempts, and calculating and returning the score.
- **`print_puzzle_outro(score)`**: Displays the score and a message based on the user’s score after the game ends.

#### Testing
This project includes a test file `test_project.py` to verify the correctness of the primary functions in `project.py`. The tests are written using `pytest`. This file tests the three core functions `game_rounds`, `get_user_selection`, and `get_user_preferences` under various scenarios, including valid and invalid user inputs, correct and incorrect guesses, and the use of hints and pass options during gameplay.

#### How to Setup:
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Cd to the project directory.
4. Run the game with `python project.py`.
5. Read the rules and follow the prompts to guess the emoji puzzles!

#### How to Play:
Playing the game is fairly simple.
1. Start the project
2. Read the rules and follow the prompts to guess the emoji puzzles!
3. Hit 'Enter' and enjoy the game

#### Design Choices:
- **CSV file**: Using a CSV file allows for easy scalability and customization of game data. The project was not too large to use a database so using csv file sounded like the best option.
- **colorama**: Since it is a terminal-based game colors are very important to make the user experience better. Colors makes the instructions more clear to see and makes the game more fun to play.
- **Levenshtein**: Most of us make typos so for better user experience Levenshtein is used to accept close enough answers as correct answers.

#### Future Enhancements:
- Add more categories and difficulty levels.
- A GUI can make the user experience much better.

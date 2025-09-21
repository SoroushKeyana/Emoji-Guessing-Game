# Emoji Guessing Game

## Overview
Emoji Guessing Game is a fun puzzle game where you guess the title of a movie, TV show, book, or video game based on a set of emojis. The game now supports both a **terminal-based version** and a **modern web-based UI**.

## Features
- Multiple categories: Movies, TV Shows, Books, Video Games
- Two difficulty levels: Easy and Hard
- Scoring system: correct answers earn points, hints earn fewer points
- Hint and Pass options
- 3 attempts per puzzle (in both UI and terminal)
- Non-repeated, randomized questions
- Beautiful, responsive web UI

## Game Rules (applies to both UI and terminal)
1. You get 1 point for each correct answer without using a hint.
2. If you use a hint, you will earn only 0.5 points for that question.
3. You have 3 attempts to guess each emoji puzzle.
4. Type "hint" to get a hint.
5. Type "pass" to pass the current question.
6. The game consists of 5 rounds. Try to score as high as possible!

## Project Structure
- `project.py`: Terminal-based game logic
- `web/app.py`: Flask web app for online play
- `web/templates/`: HTML templates for the web UI
- `data.csv`: Game data (Title, Emojis, Category, Difficulty, Hint)
- `requirements.txt`: Terminal dependencies
- `web/requirements.txt`: Web UI dependencies
- `test_project.py`: Pytest-based tests for terminal logic

## How to Play (Terminal Version)
1. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Run the game:** `python project.py`
4. Follow the prompts in your terminal.

## How to Play (Web UI)
1. **Set up a virtual environment** (you can use the same one from the terminal version).
2. **Install web dependencies:** `pip install -r requirements.txt`
3. **Run the web app:** `python web/app.py`
4. **Play the game:** Open your browser and go to `http://localhost:5000`


## Design Choices
- **CSV file**: Easy to scale and edit game data
- **Colorama**: Colorful terminal experience
- **Levenshtein**: Accepts close-enough answers for typos
- **Flask + HTML/CSS**: Modern, responsive web experience

## Future Enhancements
- Add more categories and difficulty levels
- Add animations and sound effects to the UI
- Leaderboard and multiplayer support

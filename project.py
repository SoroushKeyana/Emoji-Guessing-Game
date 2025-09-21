import csv
import random
import os
import Levenshtein
from colorama import Fore, Style, init


categories = {
    '1': 'Movies',
    '2': 'TV Shows',
    '3': 'Books',
    '4': 'Video Games',
    '5': 'Songs',
    '6': 'Famous People',
    '7': 'Countries',
}

difficulty_levels = {
    '1': 'Easy',
    '2': 'Hard'
}

rounds = 5


def main():
    init(autoreset=True)  # This line is initializing coloroma
    clear_terminal()
    welcome_message()

    try:
        get_user_preferences()
    except FileNotFoundError:
        print(Fore.RED + "Error: 'data.csv' not found. Please ensure the file exists in the current directory.")
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}")


def welcome_message():
    print('=' * 40)
    print(Style.BRIGHT + Fore.CYAN + '🎉 WELCOME TO THE EMOJI GUESSING GAME! 🎉')
    print(Style.BRIGHT + '📕 Rules of the Game:')
    print('1️⃣ You get 1 point for each correct answer without using a hint.')
    print('2️⃣ If you use a hint, you will earn only 0.5 points for that question.')
    print('3️⃣ You have 3 attempts to guess each emoji puzzle.')
    print('4️⃣ Type "hint" to get a hint.')
    print('5️⃣ Type "pass" to pass the current question.')
    print('6️⃣ The game consists of 5 rounds. Try to score as high as possible!')
    print('=' * 40)
    print(Fore.GREEN + 'Hit "Enter" to continue')
    input()


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_user_selection(options, prompt):
    print('Select a ' + prompt)

    # Displaying the available options to user
    for key, value in options.items():
        print(Style.BRIGHT + Fore.CYAN + f'{key}. {value}')

    while True:
        index = input('Type a number to select an option: ')
        if index in options:
            clear_terminal()
            return options[index]

        else:
            clear_terminal()
            print(Fore.RED + 'Invalid selection. Please try again.')

            # If invalid input show options again
            for key, value in options.items():
                print(f'{key}. {value}')


def get_user_preferences():
    clear_terminal()
    chosen_category = get_user_selection(categories, 'category:')
    chosen_level = get_user_selection(difficulty_levels, 'difficulty Level:')

    generate_puzzle(chosen_category, chosen_level)


def print_puzzle_intro():
    print(Style.BRIGHT + Fore.YELLOW + '🌟 IT\'S TIME TO GUESS! 🌟')
    print(Style.BRIGHT + Fore.GREEN + 'Here\'s your emoji puzzle:')


def game_rounds(matching_items):
    score = 0
    used_emojis = []

    for round in range(rounds):
        hint = False

        if matching_items:
            random_item = random.choice(matching_items)

            # Ensuring repeated emoji set is not appearing again for the user
            while random_item in used_emojis:
                random_item = random.choice(matching_items)

            used_emojis.append(random_item)
            correct_answer = random_item['Title']

            print('=' * 40)
            print(f'Round {round+1}')
            print(Style.BRIGHT + Fore.MAGENTA + 'What do these emojis represent?')
            print(Style.BRIGHT + f'     {random_item["Emojis"]}   ')
            print('=' * 40)

            attempts = 3
            i = 0

            while i < attempts:
                user_answer = input(f'{attempts - i} attempts left: ').lower()
                similarity = Levenshtein.ratio(user_answer.lower(), correct_answer.lower())

                if user_answer.lower() == 'hint':
                    print('Hint: ', Fore.GREEN + f'🗝️  {random_item["Hint"]} 🗝️')
                    hint = True
                    continue

                if user_answer.lower() == 'pass':
                    print(Style.BRIGHT + Fore.YELLOW + '❌ Question passed.')
                    print(f'{Style.BRIGHT + Fore.CYAN}✅ The answer is: {Fore.YELLOW + correct_answer}')
                    break

                else:
                    if similarity > 0.8:
                        if hint:
                            score += 0.5
                        else:
                            score += 1

                        print(
                            f'{Style.BRIGHT + Fore.CYAN}✅ You got it right! The answer is: {Fore.YELLOW + correct_answer}')
                        break

                    else:
                        i += 1
                        if i < attempts:
                            print('=' * 40)
                            print(Style.BRIGHT + Fore.YELLOW + ' ❌ Wrong, Try again')
                            print(Style.BRIGHT + f'   {random_item["Emojis"]}   ')
                            print('=' * 40)

                        else:
                            print('=' * 40)
                            print(f'{Style.BRIGHT + Fore.RED}💥 You’ve used all your attempts. 💥')
                            print(
                                f'{Style.BRIGHT + Fore.YELLOW}The correct answer was: {Fore.CYAN + correct_answer}')

        else:
            print('No more questions available.')

        hint = False # Resetting the hint to false for the next round
    return score


def print_puzzle_outro(score):
    if score >= 5:
        print('=' * 40)
        print('Incredible! 🌟 You\'re a master!')
    elif score >= 4:
        print('=' * 40)
        print('Great job! 👍 You\'re doing awesome!')
    elif score >= 3:
        print('=' * 40)
        print('Not bad, but there\'s room for improvement! 💪')
    else:
        print('=' * 40)
        print('Keep practicing! You\'ll get there! 🎯')
    print(f'{Style.BRIGHT + Fore.GREEN} Your score is {score}.')


def generate_puzzle(category='Movies', difficulty='Easy'):
    with open('data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        # Filtering items
        matching_items = [
            row for row in reader if row['Category'] == category and row['Difficulty'] == difficulty
        ]

        print_puzzle_intro()
        score = game_rounds(matching_items)
        print_puzzle_outro(score)


if __name__ == '__main__':
    main()

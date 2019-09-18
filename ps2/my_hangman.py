# MIT 6.0001 problem set 2
# Hangman Game

import random

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for letter in secret_word:
        if letter in letters_guessed:
            continue
        else:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    your_guess = ''
    for letter in secret_word:
        if letter in letters_guessed:
            your_guess += letter
        else:
            your_guess += '_ '
    return your_guess


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    eng_letters = 'abcdefghijklmnopqrstuvwxyz'
    available_letters = ''
    for letter in eng_letters:
        if letter in letters_guessed:
            continue
        else:
            available_letters += letter
    return available_letters


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    guess_limit = 6
    guess_counter = 0
    print('Welcome to the game Hangman! Good luck.')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    vowels = 'aeiou'
    user_guesses = ''
    warning_counter = 0
    warning_limit = 3
    print(f'You have {warning_limit - warning_counter} warnings left.')
    # Game phase.
    while is_word_guessed(secret_word, user_guesses) is not True:
        if guess_counter >= guess_limit:
            break
        avail_letters = get_available_letters(user_guesses)
        print('---------------')
        print(f'You have {guess_limit - guess_counter} guesses left.')
        print(f'Available letters: {avail_letters}.')
        print('Please guess a latter: ')
        # Guess phase.
        guess = input().lower()
        while len(guess) != 1 and str.isalpha(guess) is not True:
            if warning_counter == 3:
                print('You have no warnings left, you lose your guess')
                guess_counter += 1
            else:
                warning_counter += 1
                print(f'Oops! That is not a valid letter. You have {warning_limit - warning_counter} warnings left.')
                guess = input().lower()
        if guess in user_guesses:
            print(f'Oops! You have already guessed that letter. You now have {warning_counter + 1} warnings!')
            warning_counter += 1
        if guess in secret_word:
            user_guesses += guess
            print(f'Good guess: {get_guessed_word(secret_word, user_guesses)}')
        else:
            if guess in vowels:
                user_guesses += guess
                print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, user_guesses)}')
                guess_counter += 2
            else:
                user_guesses += guess
                print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, user_guesses)}')
                guess_counter += 1

    if is_word_guessed(secret_word, user_guesses) is not True:
        print('Sorry, you ran out of guesses.')
        print(f'My secret word was {secret_word}.')
    else:
        print('Congratulations you won!')
        remaining_guesses = guess_limit - guess_counter
        unique_letters = {}
        for letter in secret_word:
            unique_letters[letter] = 1
        total_score = remaining_guesses * len(unique_letters.keys())
        print(f'Your total score for this game is: {total_score}')


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    stripped = my_word.replace(' ', '')
    if len(stripped) == len(other_word):
        for i in range(len(stripped)):
            if stripped[i] == '_' and other_word[i] not in stripped:
                continue
            elif stripped[i] == other_word[i]:
                continue
            else:
                return False
        return True
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    matches_counter = 0
    for word in wordlist:
        result = match_with_gaps(my_word, word)
        if result is True:
            matches_counter += 1
            print(f'{word}', end=' ')

    if matches_counter == 0:
        print('No matches found.')



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    guess_limit = 6
    guess_counter = 0
    print('Welcome to the game Hangman! Good luck.')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    vowels = 'aeiou'
    user_guesses = ''
    warning_counter = 0
    warning_limit = 3
    print(f'You have {warning_limit - warning_counter} warnings left.')
    # Game phase.
    while is_word_guessed(secret_word, user_guesses) is not True:
        if guess_counter >= guess_limit:
            break
        avail_letters = get_available_letters(user_guesses)
        print('---------------')
        print(f'You have {guess_limit - guess_counter} guesses left.')
        print(f'Available letters: {avail_letters}.')
        print('Please guess a latter: ')
        # Guess phase.
        guess = input().lower()
        while guess == '*':
            print('Possible word matches are:')
            show_possible_matches(get_guessed_word(secret_word, user_guesses))
            print('')   # printing new line just to prettify the outcome.
            print(f'Available letters: {avail_letters}.')
            print('Please guess a latter: ')
            guess = input().lower()
        while len(guess) != 1 and str.isalpha(guess) is not True:
            if warning_counter == 3:
                print('You have no warnings left, you lose your guess')
                guess_counter += 1
            else:
                warning_counter += 1
                print(f'Oops! That is not a valid letter. You have {warning_limit - warning_counter} warnings left.')
                guess = input().lower()
        if guess in user_guesses:
            print(f'Oops! You have already guessed that letter. You now have {warning_counter + 1} warnings!')
            warning_counter += 1
        if guess in secret_word:
            user_guesses += guess
            print(f'Good guess: {get_guessed_word(secret_word, user_guesses)}')
        else:
            if guess in vowels:
                user_guesses += guess
                print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, user_guesses)}')
                guess_counter += 2
            else:
                user_guesses += guess
                print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, user_guesses)}')
                guess_counter += 1

    if is_word_guessed(secret_word, user_guesses) is not True:
        print('Sorry, you ran out of guesses.')
        print(f'My secret word was {secret_word}.')
    else:
        print('Congratulations you won!')
        remaining_guesses = guess_limit - guess_counter
        unique_letters = {}
        for letter in secret_word:
            unique_letters[letter] = 1
        total_score = remaining_guesses * len(unique_letters.keys())
        print(f'Your total score for this game is: {total_score}')

if __name__ == "__main__":
    ''' as default it will start game version WITH hints, if you would like
        to play version without just comment out last two lines and uncomment the two
        lines below.'''
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)





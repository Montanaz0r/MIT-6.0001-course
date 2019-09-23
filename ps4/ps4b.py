### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    is_word(word_list, 'bat') returns
    True
    is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(r" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                another letter (string).
        '''
        lowercase_alphabet = 'abcdefghijklmnopqrstuvwxyz'
        uppercase_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        shift_dictionary = {}
        if 0 <= shift < 26:
            for alphabet in (lowercase_alphabet, uppercase_alphabet):
                for letter in alphabet:
                    if letter in self.message_text:
                        shifting_range = alphabet.index(letter) + shift   # Getting letter index after shift.
                        if shifting_range > 25:   # if shifting range exceeded the range of alphabet,
                            shift_index = shifting_range - 26   # we are counting again from the beginning of alphabet.
                        else:
                            shift_index = shifting_range
                        shift_dictionary[letter] = alphabet[shift_index]
                    else:
                        shift_dictionary[letter] = letter
        else:
            print('The shift number you provided is out of range. Shift has to be integer: 0 <= shift < 26')
            return False
        return shift_dictionary


    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shift_dictionary = self.build_shift_dict(shift)
        encoded_list = []
        for cue in self.message_text:
            if cue in shift_dictionary.keys():   # Checking if cue is a letter or not(all letters are keys in the dict).
                encoded_list.append(shift_dictionary[cue])   # If so, we are appending corresponding value.
            else:
                encoded_list.append(cue)   # Else, we will just append cue.
        encoded_word = ''.join(encoded_list)   # Converts list to single word/sentence.
        return encoded_word

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        super().__init__(text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        top_matches = 0   # Records the top score for number of matches.
        solution = ()   # Opens empty tuple where the solution will be kept.
        for index in range(26):
            no_of_matches = 0
            possible_solution = self.apply_shift(index).split(' ')
            for word_index in range(len(possible_solution)):
                if is_word(self.valid_words, possible_solution[word_index]):
                    no_of_matches += 1
            if no_of_matches > top_matches:
                top_matches = no_of_matches   # Overwriting top_matches with new best score.
                solution = (26 - index, possible_solution)   # Saving index and solution for best possible_solution.
        return solution

if __name__ == '__main__':

    #1 PlaintextMessage test case.
    print('Plain test case #1')
    plaintext = PlaintextMessage('Hello, World!', 4)
    print('Expected Output: Lipps, Asvph!')
    print(f'Actual Output: {plaintext.get_message_text_encrypted()}')
    print(30 * '#')

    #2 PlaintextMessage test case.
    print('Plain test case #2')
    plaintext = PlaintextMessage('abcdef', 2)
    print('Expected Output: cdefgh')
    print(f'Actual Output: {plaintext.get_message_text_encrypted()}')
    print(30 * '#')

    #1 CiphertextMessage test case.
    print('Cipher test case #1')
    ciphertext = CiphertextMessage('Gii')
    print('Expected Output:', (2, ['Egg']))
    print(f'Actual Output: {ciphertext.decrypt_message()}')
    print(30 * '#')

    #2 CiphertextMessage test case.
    print('Cipher test case #2')
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, ['hello']))
    print(f'Actual Output: {ciphertext.decrypt_message()}')
    print(30 * '#')

    # Decrypt the bonus story.
    print('Decrypting the story bonus...')
    story = get_story_string()
    ciphertext = CiphertextMessage(story)
    print(ciphertext.decrypt_message())

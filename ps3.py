# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Mauricio Doniz
# Collaborators : 
# Time spent    : 

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*' : 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    score = 0
    score_1 = 0
    score_2 = 0
    score_2_aux = 0
    word_lower = word.lower()
    word_list = list(word_lower)
    
    for i in range (len(word_lower)):
        score_1 += SCRABBLE_LETTER_VALUES[word_list[i]]
        
    score_2_aux = (7*len(word_lower))-(3*(n-len(word_lower)))
    
    if score_2_aux > 1:
        score_2 = score_2_aux
    else:
        score_2 = 1
    
    score = score_1*score_2
    
    return score
    #return SCRABBLE_LETTER_VALUES['b']

#print(get_word_score("test", 7))

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))-1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
        
    hand['*'] = hand.get('*', 0) + 1
    
    
    for i in range(num_vowels, n-1):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
        
    return hand


#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    
    word_lower = word.lower()
    updated_hand = hand.copy()
    for i in word_lower:
        updated_hand[i] = updated_hand.get(i,0) - 1
        
    return updated_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word_lower = word.lower()
    hand_clone = hand.copy()
    
    
    if (word_lower in word_list and '*' not in word_lower):
        hand_clone = update_hand(hand_clone,word_lower) 
        for i in range (len(word_lower)):
            if(hand_clone.get(word_lower[i],0) < 0):
                return False
        return True
        
    elif ('*' in word_lower):
        wildcard_position = word_lower.find('*')
        for i in word_list:
            if(len(word_lower) == len(i)):
                if (i[wildcard_position] in VOWELS and (word_lower[0:wildcard_position] == i[0:wildcard_position] and word_lower[wildcard_position+1:] == i[wildcard_position+1:])):
                    hand_clone = update_hand(hand_clone,word_lower) 
                    for i in range (len(word_lower)):
                        if(hand_clone.get(word_lower[i],0) < 0):
                            return False
                    return True
        return False
        
    else:
        return False
    
    return False
    
#hand = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1, '*': 1}
#word_list = load_words()

#print(is_valid_word("qua*l", hand, word_list))

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    handlen = 0
    for i in hand:
        handlen += hand.get(i,0)
    return handlen


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    
    score = 0 
    
    while (calculate_handlen(hand) > 0):
        print("Current hand:")    
        display_hand(hand)
        
        word = input('Enter word, or "!!" to indicate that you are finished: ')
        
        if (word == "!!"):
            break
        
        else:
            if(is_valid_word(word, hand, word_list) == True):
                word_score = get_word_score(word, calculate_handlen(hand))
                score += word_score
                print('"',word,'" earned', get_word_score(word, calculate_handlen(hand)),"points. Total:", score, "points" )
            else:
                print("That is not a valid word. Please choose another word.")
                
        hand = update_hand(hand, word)
            
    if (word == "!!"):
        print("Terminating hand. ")
              
    else: 
        print()
        print("Ran out of letters. ")

    return score

#hand = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1, '*': 1}
#hand = {'a' : 1, 'j': 1, 'e' : 1, 'f' : 1, '*' : 1, 'r' : 1, 'x' : 1}
#hand = {'a' : 1, 'c': 1, 'f' : 1, 'i' : 1, '*' : 1, 't' : 1, 'x' : 1}
#word_list = load_words()
#play_hand(hand, word_list)

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    new_hand = hand.copy()
    VOWELS_reduced = VOWELS
    CONSONANTS_reduced = CONSONANTS
    
    for i in hand.keys():
        if i in VOWELS:
            VOWELS_reduced = VOWELS_reduced.replace(i,'')
        elif i in CONSONANTS:
            CONSONANTS_reduced = CONSONANTS_reduced.replace(i,'')
    
    if (letter in hand):
        if (letter in VOWELS):
            VOWELS_reduced = VOWELS_reduced.replace(letter,'')
            new_letter = random.choice(VOWELS_reduced)
        elif (letter in CONSONANTS):
            CONSONANTS_reduced = CONSONANTS_reduced.replace(letter,'')
            new_letter = random.choice(CONSONANTS_reduced)
        new_hand[new_letter] = new_hand.pop(letter)
    
    return new_hand
       

    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    score = 0
    print('Welcome to the Word Game. You will be given hands of 7 letters and you need to compose real words out of that set to accumulate points. You will be given a wildcard "*" which can be used as any vowel. Once you input a character, it is substracted from your hand, regardless of the validity of your word. ')
    try:
        hands = int(input ("Enter the number of hands: "))
    except ValueError:
        print("The number of hands must be an integer. Please try again. ")
        hands = 0
    hand_score = 0
    substitute_boolean = ""
    
    while (hands > 0):
        hand = deal_hand(HAND_SIZE)
        print("Current hand:")
        display_hand(hand)
        substitute_boolean = input("Would you like to substitute a letter? ")
        print()
        print(substitute_boolean)
        while (substitute_boolean.lower() != "yes" and substitute_boolean.lower() !="no"):
            print('Invalid input, please enter "yes" or "no" ')
            substitute_boolean = input("Would you like to substitute a letter? ")
            
        if(substitute_boolean == "yes" ):
            letter = input("Which letter would you like to replace: ")
            while (letter.isalpha() == False or len(letter) != 1):
                print('Invalid input, please enter a single letter of the alphabet. ')
                letter = input("Which letter would you like to replace: ")
            hand = substitute_hand(hand, letter)
                
        hand_score =play_hand(hand, word_list)
        print ("Total score for this hand: ", hand_score)
        print("----------")
        replay = input("Would you like to replay the hand? ")
        while (replay.lower() != "yes" and replay.lower() !="no"):
            print('Invalid input, please enter "yes" or "no" ')
            replay = input("Would you like to replay the hand? ")
            
        if(replay == "no"):
            score += hand_score 
            hands -=1
        elif(replay == "yes"):
            score = score
            hands = hands
        
    print("Total score over all hands: ", score)
    return score
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

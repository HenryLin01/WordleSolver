from enum import Enum
from lib2to3.pgen2.token import RIGHTSHIFT
from PyDictionary import PyDictionary
from string import ascii_lowercase

class WordleSim(object):
    length = 5
    guesses = 6

    class Result(Enum):
        CORRECT = 0
        INCORRECT = 1
        BADINPUT = 2
        LOST = 3

    def __init__(self, answer):
        self.answer = answer.lower()
        self.counter = 0
        self.correctPositions = [None for i in range(5)]
        self.correctLetters = set()
        self.incorrectLetters = set()

    def getCorrectPositions(self):
        return self.correctPositions

    def getCorrectLetters(self):
        return self.correctLetters

    def getIncorrectLetters(self):
        return self.incorrectLetters
    def guess(self, word):
        if (len(word) != WordleSim.length):
            print("length is not correct")
            return WordleSim.Result.BADINPUT

        self.counter += 1
        if self.counter > WordleSim.guesses:
            print("you are out of guesses!")
            return WordleSim.Result.LOST
            
        if word == self.answer:
            print("you guessed the correct word!")
            return  WordleSim.Result.CORRECT

        for i in range(len(word)):
            letter = word[i]
            if self.answer[i] == letter:
                self.correctPositions[i] = self.answer[i]
            
            if letter in self.answer:
                self.correctLetters.add(letter)
            else:
                self.incorrectLetters.add(letter)
            

        return WordleSim.Result.INCORRECT

class Trie(object):
    def __init__(self, words):
        root = dict()
        value = 0
        for word in words:
            word = word.lower()
            current_dict = root
            value += 1
            for letter in word:
                next_dict, next_count = current_dict.setdefault(letter, ({}, 0))
                current_dict[letter] = (next_dict, next_count + 1)
                current_dict = next_dict
        self.root = root
        self.value = value

    def isIn(self, word):
        return self.getNode(word) != (None,None)

    def getNode(self, word):
        curr_dict = self.root
        curr_value = self.value
        for letter in word:
            if letter not in curr_dict:
                return None, None
            curr_dict, curr_value = curr_dict[letter]

        return curr_dict, curr_value

class WordleSolver(object):
    
    @staticmethod
    def makeTrie(words):
        root = dict()
        for word in words:
            word = word.lower()
            current_dict = root
            for letter in word:
                next_dict, next_count = current_dict.setdefault(letter, ({}, 0))
                current_dict[letter] = (next_dict, next_count + 1)
                current_dict = next_dict
        return root

    def __init__(self, game):
        self.game = game
        # construct a trie
        with open("5_letter_words.txt", 'r') as f:
            self.trie = Trie(f.read().splitlines())
        best = 0
        best_letter = None
        for c in ascii_lowercase:
            curr_dict, curr_count = self.allWords[c]
            if curr_count > best:
                best = curr_count
                best_letter = c

        print("best letter is ", best_letter, "with value=", best)
    
    def makeGuess(self):
        correctPositions = self.game.getCorrectPositions()
        possibleLetters = set(ascii_lowercase) - self.game.incorrectLetters()
        
        guess = ""
        print("starting with guess=", guess)
        for index, letter in enumerate(correctPositions):
            if letter == None:
                best_guess = None
                best_value = 0
                for c in ascii_lowercase:

                    curr_dict, curr_value = self.trie.getNode(guess + c)
                    if curr_dict == None:
                        continue
                    elif curr_value > best_value:
                        best_guess = guess + c
                        best_value = curr_value
                print("best guess is:", best_guess, "with value=", best_value)

                # need to guess a letter at this position



def testTrie():
    words = ['apple', 'apples', 'bear', 'ber']
    badWords = ['applez', 'berr', 'chungus']
    trie = Trie(words)
    for word in words:
        assert(trie.isIn(word))
    for word in badWords:
        print(word)
        assert(not trie.isIn(word))
    print("test passed")
    # print(WordleSolver.makeTrie(['apple', 'apples', 'bear', 'ber']))

def playGame():
    import random
    with open("5_letter_words.txt", 'r') as f:
        lines = f.read().splitlines()
        myline = random.choice(lines)
        print("correct answer:", myline)
        game = WordleSim(myline)

        while True:
            guess = input("guess a word:")
            res = game.guess(guess)
            if res == WordleSim.Result.LOST:
                break
            print(game.getCorrectPositions())
            print(game.getCorrectLetters())
            print(game.getIncorrectLetters())

def generateWords():
    from english_words import english_words_set
    
    counter = 0
    with open("5_letter_words.txt", 'w') as f:
        for word in english_words_set:
            if len(word) == 5:
                print(word)
                counter += 1
                f.write(word + '\n')
    print("got ", counter)

if __name__ == "__main__":
    testTrie()
    # playGame()
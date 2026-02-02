"""
    File: writer_bot_ht.py
    Author: Alex Farbrook
    Course: CSC 120, Fall 2024
    Purpose: This program processes a text file, then uses a Markov chain
    to create new text to a desired length using a hashtable. 
    It uses prefixes and suffixes to create semi-coherent sentences.
    It then prints out this text, 10 words per line. 
"""
import random
import sys
SEED = 8
random.seed(SEED)
class Hashtable:
    """This class represents a hashtable object than stores prefixes/suffixes.

    The class defines the methods for hashtable, adding in items, getting 
    an item at a key, and hashing an item.
    """
    def __init__(self, size):
        """Creates a hashtable object of size size.

        Parameters: size is a number.
        Returns: None
        """
        self._pairs = [None] * size
        self._size = size

    def put(self, key, value):
        """Puts a value into the hashtable with key.

        Parameters: key is a string and value is also a string.
        Returns: None
        """
        index = self._hash(key)
        if self._pairs[index] is None:
            self._pairs[index] = [key, [value]]  # puts value at index if empty
            return
        ogindex = index
        while self._pairs[index] is not None:  # Linear probing
            index = (index + 1) % self._size
            if ogindex == index:
                return
        self._pairs[index] = [key, [value]]

    def get(self, key):
        """Gets the value at key.

        Parameters: key is a string.
        Returns: the value at key, or None if there is none.
        """
        index = self._hash(key)
        ogindex = index
        while self._pairs[index] is not None:  # Linear probing
            curr_key = self._pairs[index][0]
            if curr_key == key:
                return self._pairs[index][1]
            index = (index + 1) % self._size 
            if index == ogindex:  
                return None

    def __contains__(self, key):
        """Checks if the hashtable contains key.

        Parameters: key is a string.
        Returns: True if it does, and False if it doesn't.
        """
        index = self._hash(key)
        ogindex = index
        while self._pairs[index] is not None:
            curr_key = self._pairs[index][0]
            if curr_key == key:
                return True  
            index = (index + 1) % self._size  # Linear probing
            if index == ogindex:  
                return False


    def add(self, key, value):
        """Adds a value to an existing key.

        Parameters: key and value are both strings.
        Returns: None
        """ 
        index = self.get(key)
        index.append(value)

    def _hash(self, key):
        """Function taken from instructions.

        Parameters: key is a string.
        Returns: the hashed key index.
        """

        p = 0
        for c in key:
            p = 31*p + ord(c)
        return p % self._size


    def __str__(self):
        return str(self._pairs)

def get_in():
    """Gets user input for a file name, an amount of words to use as a prefix,
    a hastable size, as well as an amount of words to print.

    Parameters: None

    Returns: None
    """
    file = str(input())
    m = int(input())
    n = int(input())
    words = int(input())

    if int(n)<1:
        print("ERROR: specified prefix size is less than one")
        sys.exit(0)
    if int(words) < 1:
        print("ERROR: specified size of the generated text is less than one")
        sys.exit(0)
    NONEWORD = '@'  # creates a word that will never apear
    all_words = []
    for i in range(n):
        all_words.append(NONEWORD)  # adds the NONEWORD n times
    infile = open(file)
    for lines in infile:
        line = lines.split()
        all_words.extend(line)  # creates a list of all words in order
    table = create_table(all_words, n,m)
    gen_word = create_words(table, words, n)    # generates the new words
    print_words(gen_word)   # prints the new words
    infile.close()



def create_table(word_list, n, m):
    """Creates a table that is a hashtable of all prefixes of size n,
    as well as al of there suffixes, m entries long.

    Parameters: word_list, is a list of alll the words in the text file in
    order. n is a number that represents prefix size. m is the size 
    of the table.

    Returns: the hashtable, called table.
    """
    table = Hashtable(m)
    for num in range(len(word_list) -n):
        key_part = word_list[num: num +n]
        key = ' '.join(key_part)
        suff = word_list[num + n]
        if key in table:
            table.add(key, suff)  # adds multiple suffixes
        else:
            table.put(key,suff)
    return table

def create_words(table, word_count, n):
    """Uses a hashtable to create a list of words using a Markov 
    chain algorithm. 

    Parameters: table is a hashtable of prefixes and suffixes. 
    word_count is a number of words to create. n is a prefix size.

    Returns: the created words.
    """ 
    ret_words = []
    prefix = "@ " * n
    prefix = prefix[:-1]
    i = 0
    
    while i <= word_count -1:
        
        suffixes = table.get(prefix)
        if not suffixes:
            break
        if len(suffixes) > 1:  # checks to make sure only 1 suffix
            rand = random.randint(0, len(suffixes) -1)
            suff = suffixes[rand]
        else:
            suff = suffixes[0]
        ret_words.append(suff)
        i +=1
        prefix_words = prefix.split(" ")
        prefix_words = prefix_words[1:] + [suff]  
        prefix = " ".join(prefix_words) 
    return ret_words

def print_words(gen_words):
    """Takes in a list of words, and prints this lsit, 10 words per line.

    Parameters: gen_words are the generated words in a list.

    Returns: None
    """
    for i in range(0, len(gen_words), 10):
        print(' '.join(gen_words[i: i + 10]))


def main():
    """Calls all methods above using get_in,

    Parameters: None

    Returns: None
    """
    get_in()
main()
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:43:15 2017

@author: gsprint
"""
import random
import string
import timeit

from word_predictor import WordPredictor

def random_load_test(wp):
    '''
    
    '''
    print("random load test: ")
    VALID = string.ascii_lowercase
    TEST_NUM = 10000000
    hits = 0
    for i in range(TEST_NUM):
        prefix = ""
        for j in range(0, random.randint(1, 6), 1):
            prefix += VALID[random.randrange(0, len(VALID))]
        de = wp.get_best(prefix)
        if de.get_word() != "null":
            hits += 1
            
    print("Hit = %.2f%%" %(hits / TEST_NUM * 100))
    
def main():
    '''
    
    '''
    # train a model on the first bit of Moby Dick
    wp = WordPredictor()
    print("bad1 = %s" %wp.get_best("the"))
    wp.train("moby_start.txt")
    print("training words = %d" %(wp.get_training_count()))
    
    # try and crash things on bad input
    print("bad2 = %s" %wp.get_best("the"))
    wp.train("thisfiledoesnotexist.txt")
    print("training words = %d\n" %(wp.get_training_count()))
    
    words = ["the", "me", "zebra", "ishmael", "savage"]
    for word in words:
        print("count, %s = %d" %(word, wp.get_word_count(word)))
    wp.train("moby_end.txt")
    print()
    # check the counts again after training on the end of the book
    for word in words:
        print("count, %s = %d" %(word, wp.get_word_count(word)))
    print()
    
    # Get the object ready to start looking things up
    wp.build()
    
    # do some prefix loopups
    test = ["a", "ab", "b", "be", "t", "th", "archang"]
    for prefix in test:
        print("%s -> %s\t\t\t%.6f" %(prefix, wp.get_best(prefix), wp.get_best(prefix).get_prob()))
    print("training words = %d\n" %(wp.get_training_count()))
    
    # add two individual words to the training data
    wp.train_word("beefeater")
    wp.train_word("BEEFEATER!")
    wp.train_word("Pneumonoultramicroscopicsilicovolcanoconiosis")
 
    # The change should have no effect for prefix lookup until we build()
    print("before, b -> %s\t\t%.6f" %(wp.get_best("b"),  wp.get_best("b").get_prob()))
    print("before, pn -> %s\t\t%.6f" %(wp.get_best("pn"),  wp.get_best("pn").get_prob()))
    wp.build()
    print("after, b -> %s\t\t%.6f" %(wp.get_best("b"),  wp.get_best("b").get_prob()))
    print("after, pn -> %s\t\t%.6f" %(wp.get_best("pn"),  wp.get_best("pn").get_prob()))
    print("training words = %d\n" %(wp.get_training_count()))
    
    # test out training on a big file, timing the training as well
    start = timeit.default_timer()
    wp.train("mobydick.txt")
    wp.build()
    for prefix in test:
        print("%s -> %s\t\t\t%.6f" %(prefix, wp.get_best(prefix), wp.get_best(prefix).get_prob()))
    print("training words = %d\n" %(wp.get_training_count()))
    stop = timeit.default_timer()
    elapsed = (stop - start)
    print("elapsed (s): %.6f" %(elapsed))
    
    # test lookup using random prefixes between 1-6 characters
    start = timeit.default_timer()
    random_load_test(wp)
    stop = timeit.default_timer()
    elapsed = (stop - start)
    print("elapsed (s): %.6f" %(elapsed))
    
main()
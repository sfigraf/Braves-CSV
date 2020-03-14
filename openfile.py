import csv

import re


def openfile(file):
    f = open(file, 'rt') #rt is text mode
    reader = csv.DictReader(f, delimiter=',')
    #next(reader) #skips first row that has headers
    reader = [row for row in reader]
    return reader


#reader = openfile("bravesvideos3.csv")


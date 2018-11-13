from __future__ import unicode_literals
import csv
from hazm import *

# Initial Hazm Normalization method
normalizer = Normalizer()

# Save Text column from data.csv into a typical text file
# Delimiter for defining the rows is \n
with open('Data.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\t')
    text = []
    for row in readCSV:
        text_column = row[4]
        # Hazm Module: Apply Normalization Method for each items
        text.append(normalizer.normalize(text_column))

    # Open Input.txt then write list items to the txt file
    # Caution: First index of list should be removed cause of being a header
    text = text[1:]
    with open('Input.txt', 'w') as f:
        for item in text:
            f.write("%s\n" % item)


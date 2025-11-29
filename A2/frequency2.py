import string
import pandas as pd
from pandas import Series

class Frequency:

    def __init__(self, filename):
        '''returns a Series object that contains list of words and it's respective frequency'''

        # code from A1 returning a dictionary with words and its frequency
        with open (filename,"r") as f:
            text = f.read()

        text = text.lower() #convert to lower case

        cleaned = "" #removing punctuation
        for char in text:
            if char not in string.punctuation:  
                cleaned += char

        words = cleaned.split()  #splits words by whitespace

        count_dict = {}
        for word in words:
            if word in count_dict:
                count_dict[word] += 1
            else:
                count_dict[word] = 1

        ser = pd.Series(count_dict)  # pandas automatically uses keys as index, values as data

        self.series = ser # MUST use . (allows it to become part of the object)  instead of _ (regular variable)
       
    
    def top10(self):
        '''returns top ten frequent values'''
        # Can't do ser.nlargest as ser only exists in init.
            # access the Series by self.series

        largest_val = self.series.nlargest(10)
        return largest_val
    
    def apply_stop_list(self, stoplist):
        '''removes items that appear in the stoplist from the Series'''
        #drop removes items by index labels, in this Series, the words are the index

        #ignore if stoplist word doesn't exist in Series
        self.series = self.series.drop(stoplist, errors='ignore') 
        return self.series

    def merge(self, anotherFrequency):
        '''Adds the words and frequencies from another Frequency object. 
           Where words are the same,
           frequencies should be added. New words should be inserted, assuming a frequency of 0 in
           this object. '''

           # anotherFrequency.series instead of anotherFrequency as it would be the entire
                #frequency object and we only want the series data inside.

        # Pandas looks at all the index labels (words) from both Series 
        # For each word, it tries to get value from both Series
        # If a word is missing from one Series, fill_value=0 tells pandas "pretend it has value 0"
        # Then it adds the two values together 

        self.series = self.series.add(anotherFrequency.series, fill_value= 0)
        self.series = self.series.astype(int)
        

'''Notes'''
## Series is a data structure in pandas library for data analysis, like enhanced dictionary
# Series way (much easier!):
    # top_values = s.nlargest(3)  # Get top 3 values
    # s.drop(['apple'])           # Remove items
    # s.mean()                    # Calculate average
    # s + 10                      # Add 10 to all values

## Merge's internal logic
# result = {}
# all_words = set(self.series.index) | set(anotherFrequency.series.index)  # Union of all words

# for word in all_words:
#     # Get value from first Series, use 0 if missing
#     value1 = self.series.get(word, 0)  # .get(word, 0) returns 0 if word doesn't exist
    
#     # Get value from second Series, use 0 if missing  
#     value2 = anotherFrequency.series.get(word, 0)
    
#     # Add them together
#     result[word] = value1 + value2

# return pd.Series(result)



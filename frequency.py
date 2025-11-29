import string

def frequency(filename):
    with open (filename,"r") as f:
        text = f.read()

    text = text.lower()     #convert to lower case

    #removing punctuation
    cleaned = ""
    for char in text:
        if char not in string.punctuation:  
            cleaned += char
        #if char.isalnum() or char.isspace():
            #cleaned += char

    words = cleaned.split() #splits words by whitespace
    
    count_dict = counting(words)
    return top_ten(count_dict)

def counting(words):
    '''create a empty dictionary, if word doesn't exist, create new key and frequency pair, if word exists, add frequency by 1'''

    count_dict = {}
    for word in words:
        if word in count_dict:
            count_dict[word] += 1
        else:
            count_dict[word] = 1
    return count_dict

def top_ten(count_dict):
    '''sort the dictionary by frequency, use loop to add each of the index until the 9th position'''
    # sort by frequency (highest first)
    sorted_items = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

    # take only the first 10 and turn back into a dictionary
    return dict(sorted_items[:10])

solution = frequency("q2_sample2.txt")
#{'the': 3464, 'of': 1719, 'and': 1635, 'to': 1476, 'a': 1342, 'i': 1283, 'that': 1098, 'in': 954, 'he': 879, 'it': 866}

print(solution)


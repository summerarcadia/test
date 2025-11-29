
def frequency(filename):
    with open (filename,"r") as f:
        lines = f.readlines()

    master_list_of_words = []
    #removing punctuation
    for a_line in lines:
        a_line = a_line.lower()

        cleaned = ""
        for char in a_line: 
            if char.isalpha() or char.isspace():
                cleaned += char
            else:
                cleaned += " "  # replace punctuation with space to separate words
        
        
        words = cleaned.split() #splits word by whitespace
        master_list_of_words.extend(words) #extends the list by adding each line's words onto the []



    count_dict = counting(master_list_of_words)
    return top_ten(count_dict)

def counting(master_list_of_words):
    '''create a empty dictionary, if word doesn't exist, create new key and frequency pair, if word exists, add frequency by 1'''

    count_dict = {}
    for word in master_list_of_words:
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


# ---------------- TESTING BLOCK ----------------
if __name__ == "__main__":
    filename = "freq_test.txt"  # replace with text file

    # run your function
    result = frequency(filename)

    # print results for debugging
    print("\nTop 10 word frequencies:")
    for word, count in result.items():
        print(f"{word}: {count}")

    # show a sanity check: total number of words
    with open(filename, "r") as f:
        total_text = f.read().lower()
        print("\nTotal words (raw split):", len(total_text.split()))

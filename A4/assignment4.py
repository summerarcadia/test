import wikipedia
import nltk
import re
from pandas import Series, DataFrame
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('punkt_tab')
nltk.download('stopwords')


def getFrequencies(wiki_page):

    # Step 1: Get Wikipedia Page (auto_suggest=False to get exact match)
    page = wikipedia.page(wiki_page, auto_suggest=True)
    text = page.content

    # Step 2: Tokenize Text into Words
    tokens = word_tokenize(text)

    # Step 3: Filter Tokens (Only keep tokens with letters only)
    tokens = [token for token in tokens if re.match(r'^[a-zA-Z]+$', token)]

    # Step 4: Convert to Lowercase
    tokens = [token.lower() for token in tokens]

    # Step 5: Remove Stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Step 6: Apply Porter Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]

    # Step 7: Count Frequencies
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1

    # Step 8: Create DataFrame
    # Convert to Series
    freq_series = Series(freq_dict)
    
    # Create DataFrame
    df = DataFrame(freq_series, columns=['Frequency'])
    df.index.name = 'Term'
    
    # Sort by frequency (descending), then alphabetically for ties
    df = df.sort_index()  # First sort alphabetically
    df = df.sort_values('Frequency', ascending=False, kind='stable')  # Then by frequency (stable keeps alpha order)
    
    return df[0:30]

# Test function
result = getFrequencies("Health informatics")
print(result)
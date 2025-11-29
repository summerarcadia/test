import wikipedia
import nltk
import re
from pandas import Series, DataFrame
from nltk.tokenize import word_tokenize  # 
from nltk.corpus import stopwords  # 
from nltk.stem import PorterStemmer


nltk.download('punkt_tab')
nltk.download('stopwords')


def getFrequencies(wiki_page):

    # Get Wikipedia Page
    page = wikipedia.page(wiki_page, auto_suggest = False) # retrieves wiki page based on search term
    text = page.content #extracts text as string
    print(f"Retrieved page: {page.title}")
    print(f"Text length: {len(text)} characters")



    # Tokenize Text into Words
    tokens = word_tokenize(text)
    print(f"Number of tokens: {len(tokens)}")
    print(f"First 10 tokens: {tokens[:10]}")

    # Filter Tokens (Only want letters)
    tokens = [token for token in tokens if re.match(r'^[a-zA-Z]+$', token)]
    print(f"Number of tokens after filtering: {len(tokens)}")
    print(f"First 10 filtered tokens: {tokens[:10]}")

    # Step 4: Convert to Lowercase
    tokens = [token.lower() for token in tokens]
    
    print(f"Number of tokens: {len(tokens)}")
    print(f"First 10 tokens (lowercase): {tokens[:10]}")

    # Step 5: Remove Stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    print(f"Number of tokens after removing stopwords: {len(tokens)}")
    print(f"First 10 tokens: {tokens[:10]}")

    # Step 6: Apply Porter Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    
    print(f"Number of tokens: {len(tokens)}")
    print(f"First 10 stemmed tokens: {tokens[:10]}")

    # Step 7: Count Frequencies
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    
    print(f"Total unique terms: {len(freq_dict)}")
    print(f"Sample frequencies: {list(freq_dict.items())[:5]}")

    # Step 8: Create DataFrame
    # Convert dictionary to Series
    freq_series = Series(freq_dict)
    
    # Sort by frequency (descending), then alphabetically for ties
    freq_series = freq_series.sort_values(ascending=False, kind='mergesort')
    
    # Create DataFrame with top 30
    df = DataFrame(freq_series.head(30), columns=['Frequency'])
    df.index.name = 'Term'
    
    print(df)
    return df[0:30]

print(getFrequencies("Health informatics"))




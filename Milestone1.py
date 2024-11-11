import pandas as pd
import re

def count_word_frequencies(file_path):
    # Step 1: Read CSV file (assuming text is in the first column)
    df = pd.read_csv(file_path)

    # Combine all rows into a single string (assuming text is in the first column)
    text = ' '.join(df.iloc[:, 0].dropna().astype(str))

    # Step 2: Clean the text (remove punctuation and convert to lowercase)
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = text.lower()  # Convert to lowercase

    # Step 3: Split text into words
    words = text.split()

    # Step 4: Count word frequencies using a dictionary
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    # Step 5: Convert word counts to a pandas DataFrame
    word_freq_df = pd.DataFrame(list(word_counts.items()), columns=['Word', 'Frequency'])
    return word_freq_df


file_path = 'C:/Users/Administrator/Desktop/uST Training/Assessment/novel.csv' 

word_freq_df = count_word_frequencies(file_path)

# Display the word frequencies (Top 20 for example)
print(word_freq_df.head(20))

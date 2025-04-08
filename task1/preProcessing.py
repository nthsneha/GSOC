import pandas as pd
import re
import string
import emoji
import nltk
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("punkt_tab")

df = pd.read_csv("reddit_posts.csv")

stop_words = set(stopwords.words("english"))
custom_words = {"u","ya"}
stop_words = stop_words.union(custom_words)
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = emoji.replace_emoji(text, replace="")
    text = re.sub(r"http\S+|www\S+", "", text)  
    text = re.sub(r"@\w+|\#\w+", "", text)  
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  

    words = word_tokenize(text) 
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words] 
    
    return " ".join(words)

df["cleaned_title"] = df["title"].apply(clean_text)
df["cleaned_content"] = df["content"].apply(clean_text)

df.to_csv("cleaned_reddit_posts.csv", index=False)

print("Text preprocessing completed.")


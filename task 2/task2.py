import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/kaggle/input/sentiment-classified-posts/sentiment_classified_reddit_posts.csv")

df = df.dropna(subset=["cleaned_content"]).reset_index(drop=True)

high_risk_terms = [
    "I want to die", "I'm feeling suicidal", "I feel hopeless", "I want to hurt myself",
    "I can't go on", "I'm depressed", "Life is meaningless", "There's no point in living",
    "Nobody understands me", "I'm in so much pain", "I feel empty", "I'm scared of myself",
    "I hate my life", "I wish I could disappear", "I'm overwhelmed", "I'm broken",
    "I want everything to stop", "I'm not okay", "I'm tired of trying", "I feel trapped",
    "I feel numb", "I can't take this anymore", "Please help me", "I feel like a burden",
    "I'm in crisis", "Everything hurts", "I'm losing control", "No one cares about me",
    "I feel abandoned", "I can't breathe", "Everything feels dark", "I feel lost",
    "I cry all the time", "I’m anxious all the time", "I feel like giving up", 
    "I want the pain to end", "My life is a mess", "I'm not strong enough", "I feel so alone",
    "Nothing matters anymore", "I don’t feel safe"]

crisis_text = " ".join(high_risk_terms)

vectorizer = TfidfVectorizer()
all_texts = df["cleaned_content"].tolist() + [crisis_text]
tfidf_matrix = vectorizer.fit_transform(all_texts)

crisis_vector = tfidf_matrix[-1]
post_vectors = tfidf_matrix[:-1]

kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(post_vectors)

risk_labels = []
for i, row in df.iterrows():
    sentiment = row["sentiment"]
    post_vector = post_vectors[i]
    
    if sentiment == "Positive":
        label = "Low Risk"
    else:
        sim = cosine_similarity(post_vector, crisis_vector)[0][0]
        if sim > 0.05:  
            label = "High Risk"
        else:
            if sentiment == "Neutral":
                label = "Moderate Risk" if clusters[i] >= 1 else "Low Risk"
            else:
                label = "Moderate Risk" if clusters[i] == 0 else "Low Risk"
    
    risk_labels.append(label)

df["risk_level"] = risk_labels
df.to_csv("risk_classified_reddit_posts.csv", index=False)

print(df["risk_level"].value_counts())

distribution_table = df.groupby(["sentiment", "risk_level"]).size().unstack(fill_value=0)
print("Distribution Table (Sentiment vs Risk Level):")
print(distribution_table)

distribution_table.plot(kind='bar', stacked=True, figsize=(10, 6), colormap="coolwarm")

plt.title("Distribution of Posts by Sentiment and Risk Level")
plt.xlabel("Sentiment")
plt.ylabel("Number of Posts")
plt.legend(title="Risk Level")
plt.tight_layout()
plt.show()

similarities = cosine_similarity(post_vectors, crisis_vector)

df["crisis_similarity"] = similarities

high_risk_candidates = df[df["sentiment"] != "Positive"]
top_5_crisis_posts = high_risk_candidates.sort_values(by="crisis_similarity", ascending=False).head(5)

pd.set_option("display.max_colwidth", None)
print("Top 5 High Crisis Posts:")
print(top_5_crisis_posts[["cleaned_content", "crisis_similarity", "risk_level"]])
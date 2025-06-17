# GSOC - AI Powered Behavioral Analysis for Suicide Prevention, Substance Use and Mental Health Crisis Detection with Longitudinal Geospatial Crisis Trend Analysis.
## Key features
1. Monitor Discussions & Sentiment
2. Analyze Engagement Patterns
3. Map Crisis Trends by Location
4. Visualize Insights via Dashboard

## Tasks

### 1. Social Media Data Extraction & Preprocessing (API Handling & Text Cleaning)

- Used Reddit API to extract posts related to mental health distress, substance use or suicidality using a predefined list of 10-15 keywords to filter relevant posts.
- Stored Post ID, Timestamp, Content, Engagement Metrics (likes, comments, shares) in a structured CSV format.
- Removed stopwords, emojis and special characters for NLP preprocessing using standard NLP preprocessing techniques.
- Stored the cleaned dataset in csv format for sentiment analysis.


### 2. Sentiment & Crisis Risk Classification (NLP & Text Processing)

- Applied TextBlob for sentiment classification: A polarity score ranging from -1 to 1, indicating whether the sentiment is negative,
neutral (0), or positive. A subjectivity score ranging from 0 (objective) to 1 (highly subjective) to evaluate how factual or personal the content is.
- Used TF-IDF to detect high-risk crisis terms: Computed cosine similarity between each post’s vector and a predefined crisis vector made up of high-risk keywords.To categorize posts into risk levels, I implemented a hybrid logic combining sentiment, similarity and K-Means clustering results.
    
Logic explained:
- Positive posts were directly labeled as Low Risk, assuming no immediate crisis.
- For Neutral or Negative posts, I calculated the cosine similarity with the crisis vector: If the similarity exceeded a chosen threshold (e.g., > 0.05), the post was marked as High Risk. Else, the post’s K-Means cluster label was used to further distinguish: For Neutral sentiment: Cluster ID >= 1 suggested Moderate Risk, else Low Risk. For Negative sentiment: Cluster ID == 0 suggested Moderate Risk, else Low Risk.

### 3. Crisis Geolocation & Mapping (Basic Geospatial Analysis & Visualization)

- Extracted location mentions from Reddit posts using NLP-based place recognition.
- Used spaCy’s en_core_web_sm model to perform NER and identify GPE (Geo-Political Entities) and matched extracted locations using a GeoNames cache for fast lookup and disambiguation.
- Converted place names to coordinates using Geopy and plotted an interactive Folium heatmap to visualize crisis post clusters, displaying top 5 most-mentioned locations with highest crisis-related activity.

## Final Deliverables: 

1. A Python script that geocodes posts using spaCy + GeoNames + Geopy and generates a heatmap using Folium.
2. A visualization of regional distress patterns and a ranked list of the top 5 affected locations based on discussion volume.

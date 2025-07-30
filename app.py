import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(layout="wide")
st.title("LeapBrandWatch – Monitor LeapScholar's Online Brand Perception")

# Scrape Tweets
def fetch_tweets(query, limit=100):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        tweets.append([tweet.date, tweet.user.username, tweet.content, tweet.url])
    return pd.DataFrame(tweets, columns=["Date", "User", "Content", "URL"])

df = fetch_tweets("LeapScholar since:2025-07-20 until:2025-07-30", limit=100)

# Sentiment Analysis
def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

df["Sentiment"] = df["Content"].apply(get_sentiment)

# Display Data
st.subheader("Recent Mentions of LeapScholar")
st.dataframe(df)

# Sentiment Distribution
st.subheader("Sentiment Distribution")
sentiment_counts = df["Sentiment"].value_counts()
fig, ax = plt.subplots()
ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%", startangle=90)
st.pyplot(fig)

# Word Cloud
st.subheader("Trending Keywords")
text = " ".join(df["Content"])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
st.image(wordcloud.to_array(), use_column_width=True)

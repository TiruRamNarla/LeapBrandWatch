import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob

# Load data from CSV (sample tweets)
df = pd.read_csv("leapscholar_sample_tweets.csv")

# Analyze sentiment
def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity

df['Sentiment'] = df['content'].apply(analyze_sentiment)
df['SentimentLabel'] = df['Sentiment'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

# Streamlit UI
st.title("📊 LeapScholar Brand Perception Monitor")
st.markdown("Visualizing public sentiment around **LeapScholar** based on social media content.")

# Show raw data
if st.checkbox("Show Raw Tweet Data"):
    st.dataframe(df[['date', 'username', 'content', 'SentimentLabel']])

# Sentiment distribution
sentiment_counts = df['SentimentLabel'].value_counts()
st.subheader("Sentiment Distribution")
st.bar_chart(sentiment_counts)

# Word Cloud
st.subheader("Word Cloud of Tweets")
all_words = ' '.join(df['content'])
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# Sample Tweet Highlights
st.subheader("Sample Tweets")
for label in ['Positive', 'Negative']:
    st.markdown(f"**{label} Tweets:**")
    sample = df[df['SentimentLabel'] == label].sample(2, replace=True)
    for i, row in sample.iterrows():
        st.write(f"- {row['content']}")

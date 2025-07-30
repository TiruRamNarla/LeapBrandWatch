import pandas as pd

def fetch_sample_tweets(csv_file="leap_tweets.csv", limit=100):
    """
    Fetch tweets from a sample CSV file.
    The CSV must have columns: date, username, content, sentiment
    """
    try:
        df = pd.read_csv(csv_file)
        df['date'] = pd.to_datetime(df['date'])
        df = df.head(limit)
        return df
    except FileNotFoundError:
        print(f"⚠️ File '{csv_file}' not found. Please upload it.")
        return pd.DataFrame()

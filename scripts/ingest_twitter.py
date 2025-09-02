import snscrape.modules.twitter as sntwitter
import pandas as pd

# Search query (e.g., depression-related tweets)
query = "depression since:2024-01-01 until:2024-12-31 lang:en"
tweets = []

# Limit to 50 tweets for demo
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i>50:
        break
    tweets.append([tweet.date, tweet.user.username, tweet.content])

# Save to DataFrame
df = pd.DataFrame(tweets, columns=['date', 'user', 'tweet'])

# Save to CSV
df.to_csv("../data/twitter_ingested.csv", index=False)
print("✅ Saved to data/twitter_ingested.csv")
print(df.head())
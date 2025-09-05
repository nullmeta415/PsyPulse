import pandas as pd
try:
    import snscrape.modules.twitter as sntwitter

    print("Using snscrape to fetch live tweets..")

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
    print("Saved to data/twitter_ingested.csv")

except Exception as e:
    print("snscrape failed, falling back to mock dataset.")
    print("Error details:", e)

    # Load fallback mock dataset
    df = pd.read_csv("../data/mock_tweets.csv")
    df.to_csv("../data/twitter_ingested.csv", index=False)
    print("Mock tweetss copied to data/twitter_ingested.csv")

# Preview
print("\n=== Preview of ingested tweet ===")
print(df.head())
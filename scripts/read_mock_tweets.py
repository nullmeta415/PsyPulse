import pandas as pd
from transformers import pipeline

# 1. Load mock dataset
df = pd.read_csv("../data/mock_tweets.csv")

print("=== Preview of Tweets ===")
print(df.head())

#. 2. Load sentiment pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Iterate through and analyze tweets
print("\n=== Sentiment Analysis Results ===")
for idx, row in df.iterrows():
    result = sentiment_analyzer(row['tweet'])[0]   # returns [{'label': 'POSITIVE', 'score': 0.99}]
    # result = sentiment_analyzer([row['tweet']])[0]   # for multiple text at a time
    label = result['label']
    score = result['score']
    print(f"{row['username']} : {row['tweet']}")
    print(f"  -> Sentiment: {label} (confidence: {score:.4f})\n")


# Analyzing all tweets in one go -> much faster than looping
# results = sentiment_analyzer(df["tweet"].tolist())
# df["sentiment"] = [r["label"] for r in results]
# df["confidence"] = [round(r["score"], 3) for r in results]

# Save only the tweet, sentiment, and confidence columns
df[["tweet", "sentiment", "confidence"]].to_csv("data/mock_tweets_results.csv", index=False)

print("✅ Results saved to data/mock_tweets_results.csv")


# Plotting the graph and visuals
import matplotlib.pyplot as plt

# Count sentiment distribution
sentiment_counts = df["sentiment"].value_counts()

# Bar chart
plt.figure(figsize=(6,4))
sentiment_counts.plot(kind="bar", color=["green", "red"])
plt.title("Sentiment Distribution of Tweets")
plt.xlabel("Sentiment")
plt.ylabel("Number of Tweets")
plt.xticks(rotation=0)
plt.show()

# Pie chart
plt.figure(figsize=(5,5))
sentiment_counts.plot(kind="pie", autopct='%1.1f%%', startangle=90, colors=["green", "red"])
plt.title("Sentiment Distribution (Pie)")
plt.ylabel("")  # hide y-label
plt.show()

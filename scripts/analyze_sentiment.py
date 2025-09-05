import pandas as pd
from transformers import pipeline
import matplotlib.pyplot as plt

# === CONFIG ===
INPUT_FILE = "../data/twitter_ingested.csv" # <--- can change this to "../data/mock_tweets.csv" if needed
OUTPUT_FILE = "../data/analyzed_results.csv"

def main():
    # 1. Load input data
    df = pd.read_csv(INPUT_FILE)
    print(f"✅ Loaded {len(df)} tweets from {INPUT_FILE}")

    # 2. Initialize sentiment pipeline
    sentiment_analyzer = pipeline("sentiment-analysis")

    # 3. Run batch analysis
    results = sentiment_analyzer(df["tweet"].tolist())

    # 4. Attach results to DataFrame
    df["sentiment"] = [r["label"] for r in results]
    df["confidence"] = [round(r["score"], 3) for r in results]

    # 5. Save results
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Sentiment results saved to {OUTPUT_FILE}")

    # 6. Quick visualization
    sentiment_counts = df["sentiment"].value_counts()

    # Bar chart
    sentiment_counts.plot(kind="bar", title="Sentiment Distribution", xlabel="Sentiment", ylabel="Count", color=["red",  "green"])
    plt.show()

if __name__ == "__main__":
    main()
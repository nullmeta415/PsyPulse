# import torch
# from transformers import pipeline

# # Stage 1: Setup Check for PsyPulse
# def check_setup():
#     print("==================================")
#     print("   PsyPulse Environment Check")
#     print("==================================")

#     # Check Torch version
#     print("Torch version: ", torch.__version__)

#     # Check CUDA availability
#     if torch.cuda.is_available():
#         print("CUDA available: Yes ✅")
#         print("GPU detected: ", torch.cuda.get_device_name(0))
#         device = 0  # GPU
#     else:
#         print("CUDA available: No ❌ (using CPU)")
#         device = -1 # CPU

#     return device

# # Stage 2: First Sentiment Analysis with Hugging Face
# def model_details(nlp_model):
#     print("\n===================")
#     print("   Model Details")
#     print("===================")
#     print("Model: ", nlp_model.model.name_or_path)
#     print("Config labels: ", nlp_model.model.config.id2label)
#     print("Tokenizer vocab size: \n", nlp_model.tokenizer.vocab_size)

# def run_sentiment_analysis(device):
#     print("\n=================================")
#     print("   Sentiment Analysis Test")
#     print("=================================")

#     # Load pre-trained sentiment analysis pipeline
#     sentiment_model = pipeline("sentiment-analysis", device=device)
#     # model_details(sentiment_model)    # to get the details about the model used

#     # Example inputs
#     texts = [
#         "I love working on this project, it's amazing!",
#         "This is the worst day ever. I feel so bad.",
#         "I'm not sure how I feel about this..."
#     ]

#     for text in texts:
#         result = sentiment_model(text)[0]
#         print(f"Text: {text}")
#         print(f"-> Sentiment: {result['label']} (score: {result['score']:.4f})\n")

#--------------------------------------------------------------------------------------------------------------------

# New methods for first prototype

import json
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline

# ---------------------------
# Load Config
# ---------------------------
def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)

# ---------------------------
# 1. Ingestion (scrape or fallback)
# ---------------------------
def ingest_tweet(config):
    query = config["query"]
    limit = config["limit"]
    paths = config["paths"]

    try:
        import snscrape.modules.twitter as sntwitter
        print("Using snsrape to fetch live tweets...")

        tweets = []
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i>=limit:
                break
            tweets.append([tweet.date, tweet.user.username, tweet.content])

        df = pd.DataFrame(tweeets, columns=["date", "user", "tweet"])
        df.to_csv(paths["ingested"], index=False)
        print(f"{len(df)} live tweets saved to {paths['ingested']}")

    except Exception as e:
        print("snscrape failed, falling back to mock dataset.")
        print("Error details:", e)

        df = pd.read_csv(paths["mock"])
        df.to_csv(paths["ingested"], index=False)
        print(f"Mock tweets copied to {paths['ingested']}")

    return df

# ---------------------------
# 2. Sentiment Analysis
# ---------------------------
def analyze_sentiment(df, config):
    paths = config["paths"]
    sentiment_anlyzer = pipeline("sentiment-analysis")

    results = []
    for _, row in df.iterrows():
        text = row["tweet"]
        result = sentiment_anlyzer(text[:512])[0]   # avoid too-long texts
        results.append({
            "date": row.get("date", ""),
            "user": row.get("user", ""),
            "tweet": text,
            "sentiment": result["label"],
            "score": result["score"]
        })

    df_results = pd.DataFrame(results)
    df_results.to_csv(paths["sentiment"], index=False)
    print(f"Sentiment analysis saved to {paths['sentiment']}")
    return df_results

# ---------------------------
# 3. Visualization
# ---------------------------
def visualize_sentiment(df_results, config):
    paths = config["paths"]
    counts = df_results["sentiment"].value_counts()

    plt.figure(figsize=(6,4))
    counts.plot(kind="bar", color=["red", "green", "blue"])
    plt.title("Sentiment Distribution of Tweets")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Tweets")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig(paths["chart"])
    plt.show()
    print(f"Sentiment chart saved to {paths['chart']}")

# ---------------------------
# 4. Starting point
# ---------------------------
if __name__=="__main__":
    # device = check_setup()
    # run_sentiment_analysis(device)

    print("Starting PsyPulse pipeline...")

    config = load_config()

    df_ingested = ingest_tweet(config)
    print("\n=== Preview of ingested tweets ===")
    print(df_ingested.head())

    df_analyzed = analyze_sentiment(df_ingested, config)
    print("\n=== Preview of sentiment analysis ===")
    print(df_analyzed.head())

    visualize_sentiment(df_analyzed, config)
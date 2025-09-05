import torch
from transformers import pipeline

# Stage 1: Setup Check for PsyPulse
def check_setup():
    print("==================================")
    print("   PsyPulse Environment Check")
    print("==================================")

    # Check Torch version
    print("Torch version: ", torch.__version__)

    # Check CUDA availability
    if torch.cuda.is_available():
        print("CUDA available: Yes ✅")
        print("GPU detected: ", torch.cuda.get_device_name(0))
        device = 0  # GPU
    else:
        print("CUDA available: No ❌ (using CPU)")
        device = -1 # CPU

    return device

# Stage 2: First Sentiment Analysis with Hugging Face
def model_details(nlp_model):
    print("\n===================")
    print("   Model Details")
    print("===================")
    print("Model: ", nlp_model.model.name_or_path)
    print("Config labels: ", nlp_model.model.config.id2label)
    print("Tokenizer vocab size: \n", nlp_model.tokenizer.vocab_size)

def run_sentiment_analysis(device):
    print("\n=================================")
    print("   Sentiment Analysis Test")
    print("=================================")

    # Load pre-trained sentiment analysis pipeline
    sentiment_model = pipeline("sentiment-analysis", device=device)
    # model_details(sentiment_model)    # to get the details about the model used

    # Example inputs
    texts = [
        "I love working on this project, it's amazing!",
        "This is the worst day ever. I feel so bad.",
        "I'm not sure how I feel about this..."
    ]

    for text in texts:
        result = sentiment_model(text)[0]
        print(f"Text: {text}")
        print(f"-> Sentiment: {result['label']} (score: {result['score']:.4f})\n")



if __name__=="__main__":
    device = check_setup()
    run_sentiment_analysis(device)
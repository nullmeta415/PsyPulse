import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

# 1. Choose the same model as pipeline("sentiment-analysis") uses
model_name = "distilbert-base-uncased-finetuned-sst-2-english"

# 2. Load tokenizer + model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 3. Example text
text = "I really love working on this project!"

# 4. Tokenization step
inputs = tokenizer(text, return_tensors="pt")   # pt = PyTorch
print("=== Tokenization ===")
print("Input text:", text)
print("Token IDs:", inputs["input_ids"])
print("Attention mask:", inputs["attention_mask"])
print("Decoded back:", tokenizer.decode(inputs["input_ids"][0]))

# 5. Forward pass through the model
with torch.no_grad():   # no training, just inference
    outputs = model(**inputs)

# 6. Raw model outputs (logits)
logits = outputs.logits
print("\n=== Raw logits (before softmax) ===")
print(logits)

# 7. Convert to probabilities
probs = F.softmax(logits, dim=-1)
print("\n=== Probablities (after softmax) ===")
print(probs)

# 8. Map class IDs to labels
predict_class_id = probs.argmax().item()
label = model.config.id2label[predict_class_id]
score = probs[0][predict_class_id].item()

print("\n=== Final Prediction ===")
print(f"Lable: {label}, Score: {score:.4f}")
from scraper import get_top_stories
from sentiment import get_sentiment_score, too_negative

abstracts = get_top_stories()

texts = [
    "I absolutely hate this. It's terrible!",
    "This is okay, not great but not bad.",
    "I love this product! It's fantastic!"
]

#for entry in abstracts:
filtered_texts = [text for text in abstracts if not too_negative(text)]

print("Filtered Texts (Not Too Negative):")
print(filtered_texts)
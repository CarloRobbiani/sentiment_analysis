from scraper import get_top_stories_ny_times
from sentiment import get_sentiment_score, too_negative

articles = get_top_stories_ny_times()


#for entry in abstracts:
filtered_texts = [text for text in articles if not too_negative(text["abstract"])]

print("Filtered Texts (Not Too Negative):")
print(filtered_texts)

## Deploy using the streamlit cloud? ##
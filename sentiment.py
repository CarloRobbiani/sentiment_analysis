from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download the VADER lexicon if not already downloaded
nltk.download('vader_lexicon')

def get_sentiment_score(text):
    """
    Take a string input and return its sentiment score.
    The score is a dictionary containing 'neg', 'neu', 'pos', and 'compound' scores.
    """
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    return sentiment

def too_negative(text, threshold = -0.5):
    """
    Test if the text is too negative based on the specified threshold.
    Return True if the text is too negative, False otherwise.
    """

    score = get_sentiment_score(text)
    return score["compound"] < threshold


if __name__ == "__main__":
    text = "I love this product! It's absolutely amazing."
    print(get_sentiment_score(text))

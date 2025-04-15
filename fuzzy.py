import numpy as np
import skfuzzy as fuzz

def trapezoidal(x, a, b, c, d):
    return max(min((x - a)/(b - a), 1, (d - x)/(d - c)), 0)

def sentiments(compound_score):
    sentiments = {
        'Negative': trapezoidal(compound_score, -1.0, -0.9, -0.6, -0.3),
        'Somewhat Negative': trapezoidal(compound_score, -0.6, -0.3, -0.1, 0.1),
        'Neutral': trapezoidal(compound_score, -0.2, 0.0, 0.0, 0.2),
        'Somewhat Positive': trapezoidal(compound_score, 0.1, 0.3, 0.5, 0.6),
        'Positive': trapezoidal(compound_score, 0.3, 0.7, .9, 1.0)
    }
    return sentiments


def fuzzy(compound_score, threshold):
    """Create a fuzzy membership using the trapezoidal function.
    Based on that create a method to filter out texts that are classified as too negative.

    :compound_score: The score from the vader lexicon
    :threshold: The user specified threshold
    """
    # Create universe of scores (-1 to 1)
    x_sentiment = np.arange(-1, 1.01, 0.01)

    # Fuzzy membership functions
    very_neg = fuzz.trapmf(x_sentiment, [-1, -1, -0.75, -0.5])
    neg = fuzz.trimf(x_sentiment, [-0.75, -0.5, 0])
    neutral = fuzz.trimf(x_sentiment, [-0.1, 0, 0.1])
    pos = fuzz.trimf(x_sentiment, [0, 0.5, 0.75])
    very_pos = fuzz.trapmf(x_sentiment, [0.5, 0.75, 1, 1])

    score = compound_score

    membership = {
        "very_neg": fuzz.interp_membership(x_sentiment, very_neg, score),
        "neg": fuzz.interp_membership(x_sentiment, neg, score),
        "neutral": fuzz.interp_membership(x_sentiment, neutral, score),
        "pos": fuzz.interp_membership(x_sentiment, pos, score),
        "very_pos": fuzz.interp_membership(x_sentiment, very_pos, score),
    }
    print(membership)

    # Some arbitrary method, can be changed
    neg_score = max(membership['very_neg'], membership['neg'])
    pos_score = max(membership['pos'], membership['very_pos'])

    fuzzy_negative = neg_score - pos_score  # A sort of balance metric
    if fuzzy_negative > threshold:
        print("Too negative")
    else:
        print("Not too negative")



if __name__=="__main__":
    fuzzy(0.6)

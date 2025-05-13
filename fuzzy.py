import numpy as np
import skfuzzy as fuzz
import streamlit as st

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


def fuzzy_membership(compound_score, threshold, very_neg=-0.5, neg=0, pos=0, very_pos=0.5):
    """Create a fuzzy membership using the trapezoidal function.
    Based on that create a method to filter out texts that are classified as too negative.

    :compound_score: The score from the vader lexicon
    :threshold: The user specified threshold
    :very_neg: The adjustable falloff for the very negative curve
    :neg: The adjustable falloff for the negative curve
    :pos: The adjustable rise of the positive curve
    :very_pos: The adjustable rise of the very positive curve
    """
    # Create universe of scores (-1 to 1)
    x_sentiment = np.arange(-1, 1.01, 0.01)

    # Fuzzy membership functions
    very_neg = fuzz.trapmf(x_sentiment, [-1, -1, -0.75, very_neg])
    neg = fuzz.trimf(x_sentiment, [-0.75, -0.5, neg])
    neutral = fuzz.trimf(x_sentiment, [-0.1, 0, 0.1])
    pos = fuzz.trimf(x_sentiment, [pos, 0.5, 0.75])
    very_pos = fuzz.trapmf(x_sentiment, [very_pos, 0.75, 1, 1])

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
    # if fuzzy_negative > threshold:
    #     print("Too negative")
    #     return False
    # else:
    #     print("Not too negative")
    #     return True

    decision = fuzzy_negative <= threshold

    return decision, membership

import matplotlib.pyplot as plt
def plot_trapezoid():

    # Define sentiment range from -1 to 1 with 0.01 resolution
    x_sentiment = np.arange(-1, 1.01, 0.01)

    # Create membership functions
    very_neg = fuzz.trapmf(x_sentiment, [-1, -1, -0.75, -0.5])  # Full trapezoid left
    neg = fuzz.trimf(x_sentiment, [-0.75, -0.5, 0])             # Triangular left
    neutral = fuzz.trimf(x_sentiment, [-0.1, 0, 0.1])           # Narrow triangular center
    pos = fuzz.trimf(x_sentiment, [0, 0.5, 0.75])               # Triangular right
    very_pos = fuzz.trapmf(x_sentiment, [0.5, 0.75, 1, 1])     # Full trapezoid right

    # Plot configuration
    plt.figure(figsize=(10, 6))
    plt.plot(x_sentiment, very_neg, label='Very Negative')
    plt.plot(x_sentiment, neg, label='Negative')
    plt.plot(x_sentiment, neutral, label='Neutral')
    plt.plot(x_sentiment, pos, label='Positive')
    plt.plot(x_sentiment, very_pos, label='Very Positive')

    plt.title('Fuzzy Sentiment Membership Functions')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Membership Degree')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_trapezoid_app(very_neg, neg, pos, very_pos):
    """Plots the trapezoid in the streamlit app
    """
    # Define sentiment range from -1 to 1 with 0.01 resolution
    x_sentiment = np.arange(-1, 1.01, 0.01)

    # Create membership functions using slider values
    very_neg_curve = fuzz.trapmf(x_sentiment, [-1, -1, -0.75, very_neg])
    neg_curve = fuzz.trimf(x_sentiment, [-0.75, -0.5, neg])
    neutral_curve = fuzz.trimf(x_sentiment, [-0.1, 0, 0.1])
    pos_curve = fuzz.trimf(x_sentiment, [pos, 0.5, 0.75])
    very_pos_curve = fuzz.trapmf(x_sentiment, [very_pos, 0.75, 1, 1])

    # Plot configuration
    plt.figure(figsize=(10, 6))
    plt.plot(x_sentiment, very_neg_curve, label='Very Negative')
    plt.plot(x_sentiment, neg_curve, label='Negative')
    plt.plot(x_sentiment, neutral_curve, label='Neutral')
    plt.plot(x_sentiment, pos_curve, label='Positive')
    plt.plot(x_sentiment, very_pos_curve, label='Very Positive')

    plt.title('Fuzzy Sentiment Membership Functions')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Membership Degree')
    plt.legend()
    plt.grid(True)
    st.sidebar.pyplot(plt)  # Use Streamlit's pyplot to display the plot

if __name__=="__main__":
    #fuzzy(0.6)
    plot_trapezoid()

import streamlit as st
from scraper import get_top_stories_ny_times
from sentiment import too_negative, get_sentiment_score
from fuzzy import fuzzy_membership, plot_trapezoid_app



def display_articles(articles):
    """ Displays the articles in a nice way.
    
    :articles: The articles from the NY Times api as a list
    """
    # for article in articles:
    #     st.header(article["title"])
    #     st.write(f"{article.get('byline', 'Unknown')} | **Source:** {article.get('section', 'Unknown')}")
    #     st.write(article["abstract"])
    #     # If there is a picture show the picture
    #     if "multimedia" in article and article["multimedia"]:
    #         st.image(article["multimedia"][0]["url"], caption=article["multimedia"][0]["caption"])
    #     # Show a link to the original article
    #     st.write(f"[Read more]({article['url']})")
    #     st.markdown("---")
    # 
    for article in articles:
        st.header(article["title"])
        
        byline = article.get("byline", "Unknown")
        section = article.get("section", "Unknown")
        
        # Get sentiment display
        sentiment_display = "Neutral"
        if "membership" in article:
            membership = article["membership"]
            active_sentiments = []
            
            for key, label in [
                ("very_neg", "Very Negative"),
                ("neg", "Negative"),
                ("neutral", "Neutral"),
                ("pos", "Positive"),
                ("very_pos", "Very Positive")
            ]:
                if membership[key] > 0.1:
                    active_sentiments.append(f"{label} ({membership[key]:.2f})")
            
            sentiment_display = ", ".join(active_sentiments) if active_sentiments else "Neutral"

        st.write(f"{byline} | Source: {section} | Sentiment: {sentiment_display}")
        st.write(article["abstract"])

        if "multimedia" in article and article["multimedia"]:
            st.image(article["multimedia"][0]["url"], 
                   caption=article["multimedia"][0].get("caption", ""))
        
        st.write(f"[Read more]({article['url']})")
        st.markdown("---")


def main():
    st.title("News Sentiment Filter")
    st.write("This app filters the news based on the given sentiment")

    # Settings sidebar with sliders
    st.sidebar.header("Settings", help="""Adjust the sliders to determine how much news get filtered put.
                       Generally the more right a slider is, the more news get filtered out.""")
    very_pos = st.sidebar.slider("Choose a threshold for very positive curve", -1.0, 0.75, 0.5)
    positive = st.sidebar.slider("Choose a threshold for positive curve", -1.0, 0.5, 0.25)
    negative = st.sidebar.slider("Choose a threshold for negative curve", -0.5, 1.0, -0.25)
    very_neg = st.sidebar.slider("Choose a threshold for very_negative curve", -0.75, 1.0, -0.5)

     # Plot the trapezoid membership functions in the sidebar
    plot_trapezoid_app(very_neg, negative, positive, very_pos)

    positive_focus = (
    very_pos > 0.5 and
    positive > 0.25 and
    negative > 0 and
    very_neg > -0.25
    )

    negative_focus = (
    very_neg < -0.5 and
    negative < -0.25 and
    positive < 0.0 and
    very_pos < 0.25
    )

    if positive_focus and not negative_focus:
        filter_mode = "Most Positive"
    elif negative_focus and not positive_focus:
        filter_mode = "Most Negative"
    else:
        filter_mode = "Balanced"

    # Auto-adjust threshold
    if filter_mode == "Most Positive":
        threshold = 0.05
    elif filter_mode == "Most Negative":
        threshold = 1.0
    else:
        threshold = 0.1


    # Button to start the scraping
    if st.button("Show news"):
        # Get the stories
        articles = get_top_stories_ny_times()

        # Filter texts based on chosen thresholds
        #filtered_texts = [text for text in articles if not too_negative(text["abstract"], positive)]
        # filtered_texts = [text for text in articles if fuzzy_membership(get_sentiment_score(text["abstract"])["compound"], 
        #                                                                          threshold,
        #                                                                          very_neg, negative, positive, very_pos)]
        # # Show results
        # display_articles(filtered_texts)
        processed_articles = []

        for article in articles:
            sentiment = get_sentiment_score(article["abstract"])
            # Get both filter decision and membership values
            should_include, membership = fuzzy_membership(
                sentiment["compound"],
                threshold,
                very_neg,
                negative,
                positive,
                very_pos
            )
            
            if should_include:
                article["membership"] = membership
                processed_articles.append(article)

        display_articles(processed_articles)

if __name__ == "__main__":
    main()
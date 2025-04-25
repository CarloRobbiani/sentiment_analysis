import streamlit as st
from scraper import get_top_stories_ny_times
from sentiment import too_negative, get_sentiment_score
from fuzzy import fuzzy_membership

def display_articles(articles):
    """ Displays the articles in a nice way.
    
    :articles: The articles from the NY Times api as a list
    """
    for article in articles:
        st.header(article["title"])
        st.write(f"**By:** {article.get('byline', 'Unknown')} | **Source:** {article.get('section', 'Unknown')}")
        st.write(article["abstract"])
        # If there is a picture show the picture
        if "multimedia" in article and article["multimedia"]:
            st.image(article["multimedia"][0]["url"], caption=article["multimedia"][0]["caption"])
        # Show a link to the original article
        st.write(f"[Read more]({article['url']})")
        st.markdown("---")


def main():
    st.title("News Sentiment Filter")
    st.write("This app filters the news based on the given sentiment")

    # Settings sidebar with sliders
    st.sidebar.header("Settings")
    very_pos = st.sidebar.slider("Choose a threshold for very positive curve", -1.0, 1.0, 0.5)
    positive = st.sidebar.slider("Choose a threshold for positive curve", -1.0, 1.0, 0.0)
    very_neg = st.sidebar.slider("Choose a threshold for very_negative curve", -1.0, 1.0, 0.0)
    negative = st.sidebar.slider("Choose a threshold for negative curve", -1.0, 1.0, -0.5)
    

    # Button to start the scraping
    if st.button("Show news"):
        # Get the stories
        articles = get_top_stories_ny_times()

        # Filter texts based on chosen thresholds
        #filtered_texts = [text for text in articles if not too_negative(text["abstract"], positive)]
        filtered_texts = [text for text in articles if fuzzy_membership(get_sentiment_score(text["abstract"])["compound"], 
                                                                                 0.5,
                                                                                 very_neg, negative, positive, very_pos)]
        # Show results
        display_articles(filtered_texts)

if __name__ == "__main__":
    main()
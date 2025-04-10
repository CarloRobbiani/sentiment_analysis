import streamlit as st
from scraper import get_top_stories_ny_times
from sentiment import too_negative

def display_articles(articles):
    """ Displays the articles in a nice way.
    Keyword arguments:
    articles -- The articles from the NY Times api
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
    positive = st.sidebar.slider("Choose a threshold for positive values", -1.0, 1.0, 0.0)
    neutral = st.sidebar.slider("Choose a threshold for neutral values", -1.0, 1.0, 0.0)
    negative = st.sidebar.slider("Choose a threshold for negative values", -1.0, 1.0, 0.0)
    

    # Button to start the scraping
    if st.button("Show news"):
        # Get the stories
        articles = get_top_stories_ny_times()

        # Filter texts based on chosen thresholds
        filtered_texts = [text for text in articles if not too_negative(text["abstract"], positive)]
        
        # Show results
        display_articles(filtered_texts)

if __name__ == "__main__":
    main()
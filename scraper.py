import requests
import streamlit as st


# Replace with your NYT API key
API_KEY = st.secrets["api_keys"]["nyt_api_key"]
URL = f"https://api.nytimes.com/svc/topstories/v2/home.json?api-key={API_KEY}"

def get_top_stories_ny_times(nr_articles = 15):
    """
    Use the New York Times api to get the top stories.
    Return the articles as a list.

    :nr_articles: the number of articles to return
    """
    response = requests.get(URL)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("results", [])
        # articles contain section, subsection, title, abstract, url
        art = []
        
        if len(articles) < nr_articles:
            nr_articles = len(articles)
        for i, article in enumerate(articles[:nr_articles], 1):  # Get top 10 stories
            """ print(f"{i}. {article['title']}")
            print(f"   {article['abstract']}")
            print(f"   {article['url']}\n") """
            art.append(article)
    else:
        print(f"Error: Unable to fetch news (Status Code: {response.status_code})")
    return art



if __name__ == "__main__":
    get_top_stories_ny_times()


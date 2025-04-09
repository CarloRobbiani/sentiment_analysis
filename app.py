import streamlit as st
from scraper import get_top_stories
from sentiment import too_negative

def main():
    st.title("News Sentiment Filter")
    st.write("This app filters the news based on the given sentiment")

    # Sliders for the filtering still to be used
    positive = st.slider("Choose a threshold for positive values", -1.0, 1.0, 0.0)
    neutral = st.slider("Choose a threshold for neutral values", -1.0, 1.0, 0.0)
    negative = st.slider("Choose a threshold for negative values", -1.0, 1.0, 0.0)

    # Button to start the scraping
    if st.button("Show news"):
        # Get the stories
        texts = get_top_stories()

        # Filter texts based on chosen thresholds
        filtered_texts = [text for text in texts if not too_negative(text, positive)]
        
        # Show results
        if filtered_texts:
            st.subheader("Filtered messages")
            for i, text in enumerate(filtered_texts):
                st.write(f"{i + 1}. {text}")
        else:
            st.write("No messages match the criteria")

if __name__ == "__main__":
    main()
import streamlit as st
from scraper import get_top_stories
from sentiment import too_negative

def main():
    st.title("News Sentiment Filter")
    st.write("This app filters the news based on the given sentiment")

    # Slider für den Schwellenwert
    threshold = st.slider("Choose a threshold", -1.0, 1.0, 0.0)

    # Button zum Abrufen der Nachrichten
    if st.button("Show news"):
        # Nachrichten abrufen
        texts = get_top_stories()

        # Nachrichten filtern
        filtered_texts = [text for text in texts if not too_negative(text, threshold)]
        
        # Ergebnisse anzeigen
        if filtered_texts:
            st.subheader("Filtered messages")
            for i, text in enumerate(filtered_texts):
                st.write(f"{i + 1}. {text}")
        else:
            st.write("No messages match the criteria")

if __name__ == "__main__":
    main()
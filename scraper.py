import requests
import secret_key

# Replace with your NYT API key
API_KEY = secret_key.API_KEY
URL = f"https://api.nytimes.com/svc/topstories/v2/home.json?api-key={API_KEY}"

def get_top_stories():
    response = requests.get(URL)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("results", [])
        
        for i, article in enumerate(articles[:10], 1):  # Get top 10 stories
            print(f"{i}. {article['title']}")
            print(f"   {article['abstract']}")
            print(f"   {article['url']}\n")
    else:
        print(f"Error: Unable to fetch news (Status Code: {response.status_code})")

if __name__ == "__main__":
    get_top_stories()


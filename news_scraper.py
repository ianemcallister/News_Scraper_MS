import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_google_news(company_name):
    # Prepare the search URL
    search_url = f"https://news.google.com/search?q={company_name}&hl=en-US&gl=US&ceid=US%3Aen"
    response = requests.get(search_url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve news articles")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all news articles
    articles = soup.find_all('article')

    # List to store article data
    news_data = []

    for article in articles:
        # Extract title, link, and publication date
        title = article.find('h3').text if article.find('h3') else "No Title"
        link = article.find('a')['href']
        if link.startswith('./'):
            link = 'https://news.google.com' + link[1:]  # Correcting relative links
        pub_date = article.find('time')['datetime'] if article.find('time') else datetime.now().isoformat()

        # Append article data to the list
        news_data.append({
            'title': title,
            'link': link,
            'published_date': pub_date,
            'company': company_name
        })

    return news_data

def main():
    companies = ['Webflow']  # Add the companies you want to track
    all_articles = []

    for company in companies:
        articles = scrape_google_news(company)
        all_articles.extend(articles)

    # Convert the articles to a DataFrame and save to CSV
    df = pd.DataFrame(all_articles)
    df.to_csv('news_articles.csv', index=False)
    print(df)
    print("News articles collected and saved to news_articles.csv")

if __name__ == "__main__":
    main()

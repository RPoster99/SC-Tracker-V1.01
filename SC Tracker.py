import tweepy
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
client = tweepy.Client(bearer_token=bearer_token)
print("Bearer Token:", os.getenv('TWITTER_BEARER_TOKEN'))
def get_tweets_by_keyword_v2(keyword, max_tweets):
    tweets_list = []
    for tweet in tweepy.Paginator(client.search_recent_tweets, query=keyword,
                                  tweet_fields=['author_id', 'created_at', 'text'],
                                  max_results=100).flatten(limit=max_tweets):
        tweet_data = {
            'user': tweet.author_id,
            'text': tweet.text,
            'created_at': tweet.created_at
        }
        tweets_list.append(tweet_data)
    return tweets_list
tweets_wms = get_tweets_by_keyword_v2("BlueYonder WMS", 10)
tweets_wes = get_tweets_by_keyword_v2("BlueYonder WES", 10)
tweets_combined = tweets_wms + tweets_wes
URL = 'https://www.gartner.com/en/newsroom/topics/supply-chain'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all('div', class_='curated-related-body')
for curated_related_body in results:
    title = curated_related_body.find('h2').text if curated_related_body.find('h2') else 'No Title'
    summary = curated_related_body.find('p').text if curated_related_body.find('p') else 'No Summary'
    print(f"Title: {title}\nSummary: {summary}\n")
tweets_df = pd.DataFrame(tweets_combined)
tweets_df.to_csv('tweets.csv', index=False)

# pipenv install tweepy
import os
import tweepy
import requests
from dotenv import load_dotenv

load_dotenv()

x_client = tweepy.Client(
    bearer_token= os.getenv("X_BEARER_TOKEN"),
    consumer_key= os.getenv("X_API_KEY"),
    consumer_secret= os.getenv("X_API_KEY_SECRET"),
    access_token= os.getenv("X_ACCESS_TOKEN"),
    access_token_secret= os.getenv("X_ACCESS_TOKEN_SECRET"),
)

def scrape_user_tweets(username:str, num_tweets:int = 5, mock = True) -> list:
    """
    Scrapes a Twitter or X user's original tweets (i.e. no retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """
    post_list = []

    if mock:
        url_mock = "https://gist.githubusercontent.com/Xander31/47db0308b06e4806c04359a424100e6b/raw/04dfd41da31a9edfdd65766a0f5cdfe312fb955c/post_X_example"
        x_posts = requests.get(
            url=url_mock,
            timeout=10,
        ).json()

    else:
        user_id = x_client.get_user(username=username).data.id
        x_posts = x_client.get_users_tweets(
            id= user_id,
            max_results= num_tweets,
            exclude=["retweets", "replies"]
        )
        x_posts = x_posts.data

    for post in x_posts:
        post_dict = {}
        post_dict["text"] = post["text"]
        post_dict["url"] = f"https://x.com/{username}/status/{post['id']}"
        post_list.append(post_dict)

    return post_list

if __name__ == "__main__":
    tweets = scrape_user_tweets(username="EdenMarco177", mock= True)
    print(tweets)
    print("XD!")
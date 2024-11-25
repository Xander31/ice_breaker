# pipenv install tweepy



def scrape_user_tweets(username:str, num_tweets:int = 5, mock = True) -> str:
    """
    Scrapes a Twitter or X user's original tweets (i.e. no retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """


if __name__ == "__main__":
    tweets = scrape_user_tweets(username="")
    print(tweets)
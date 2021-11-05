import configparser
import praw


class RedditClient:
    reddit_client_instance = None

    @staticmethod
    def get_instance():
        if RedditClient.reddit_client_instance == None:
            RedditClient()
        return RedditClient.reddit_client_instance

    def __init__(self):
        """
        Construct the singleton instance with the creds
        """
        if RedditClient.reddit_client_instance != None:
            raise Exception("Instance already exists")
        else:
            config = configparser.ConfigParser()
            config.read("config.ini")
            reddit_client = praw.Reddit(
                client_id=config["REDDIT"]["client_id"],
                client_secret=config["REDDIT"]["client_secret"],
                user_agent=config["REDDIT"]["user_agent"],
            )
            RedditClient.reddit_client_instance = reddit_client

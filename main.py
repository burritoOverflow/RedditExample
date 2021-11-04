import configparser
import logging
import sys
import argparse
import praw
from praw.models import MoreComments

config = configparser.ConfigParser()
config.read("config.ini")
reddit = praw.Reddit(
    client_id=config["REDDIT"]["client_id"],
    client_secret=config["REDDIT"]["client_secret"],
    user_agent=config["REDDIT"]["user_agent"],
)


def fetch_submissions(subreddit: str, limit: str) -> list[str]:
    """
    Given a subreddit, fetch all submissions (up to the limit)
    Defaults to /hot submissions
    """
    logging.info(f"Fetching {limit} submission from subreddit {subreddit}")
    submission_list = list()
    for submission in reddit.subreddit(subreddit).hot(limit=limit):
        submission_list.append(submission)
    logging.info(f"{limit} Submissions fetched")
    return submission_list


def get_comments(submission: dict) -> dict:
    logging.info(f"Fetching from {submission.title}")
    # return {submission.title: [comment.body for comment in submission.comments]}
    submission_comment_dict = {"title": submission.title, "comments": list()}
    for comment in submission.comments:
        # for now, only get top-level comments, not threads on those comments
        # see: https://praw.readthedocs.io/en/stable/tutorials/comments.html for exp
        if isinstance(comment, MoreComments):
            continue
        else:
            submission_comment_dict["comments"].append(comment.body)
    logging.info(
        f"Got {len(submission_comment_dict['comments'])} comments on submission: {submission_comment_dict['title']}"
    )
    return submission_comment_dict


def log_comments(comments: dict) -> None:
    title = comments["title"]
    comments = comments["comments"]
    logging.info(f"Submission {title} has {len(comments)} comments")
    for i, comment in enumerate(comments):
        logging.info(f"Comment {i} {comment}")


def main():
    logging.basicConfig(
        filename="reddit.log",
        filemode="a",
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--subreddit",
        help="the subreddit for submissions and comments",
    )
    args = parser.parse_args()
    if args.subreddit:
        submission_list = fetch_submissions(args.subreddit, 10)
        for s in submission_list:
            comments_dict = get_comments(s)
            log_comments(comments_dict)
    else:
        print("usage: python3 main.py <subreddit>")
        sys.exit(1)


if __name__ == "__main__":
    main()

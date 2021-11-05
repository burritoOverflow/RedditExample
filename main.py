import logging
import sys
import reddit_client
import util
from praw.models import MoreComments

reddit_client = reddit_client.RedditClient.get_instance()


def fetch_submissions(subreddit: str, limit: str) -> list[str]:
    """
    Given a subreddit, fetch all submissions (up to the limit)
    using /hot submissions, here
    """
    logging.info(f"Fetching {limit} submission from subreddit {subreddit}")
    submission_list = list()
    # change this argument from hot to get new, for example
    for submission in reddit_client.subreddit(subreddit).hot(limit=limit):
        submission_list.append(submission)
    logging.info(f"{limit} Submissions fetched")
    return submission_list


def get_comments(submission: dict) -> dict:
    """
    Given a submission, traverse the top level comments and create
    and return a dict of those comments where {k: v} is {submissionTitle: [comments]}
    """
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
    """
    For now, just write the comments to a log (for demo)
    """
    title = comments["title"]
    comments = comments["comments"]
    log_str = f"Submission {title} has {len(comments)} comments"
    logging.info(log_str)
    print(log_str)
    for i, comment in enumerate(comments):
        logging.info(f"Comment {i} {comment}")


def main():
    util.set_logging_config()
    args = util.create_args()
    arg_tuple = (args.subreddit, args.numcomments, args.numsubmissions)
    if all(arg_tuple):
        submission_list = fetch_submissions(args.subreddit, args.numsubmissions)
        for s in submission_list:
            comments_dict = get_comments(s)
            log_comments(comments_dict)
    else:
        print(
            "usage: python3 main.py -s <subreddit> -n <numcomments> -c <numsubmissions>"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

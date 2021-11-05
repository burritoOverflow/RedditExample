import datetime
import logging
import os
import argparse


def create_log_dir() -> str:
    """
    Create log dir if not exists
    """
    cwd = os.getcwd()
    log_dir = os.path.join(cwd, r"logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    else:
        print(f"created log dir at: {log_dir}")
    return log_dir


def set_logging_config():
    """
    Set the logging configuration to be unique for each invocation
    """
    d = datetime.datetime.now().strftime("%I_%M%p_%B_%d_%Y")
    log_dir = create_log_dir()
    f_name = f"{log_dir}/{d}_reddit.log"
    logging.basicConfig(
        filename=f_name,
        filemode="a",
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def create_args() -> argparse.Namespace:
    """
    Set the command line args for the reddit client
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--subreddit",
        help="the subreddit for submissions and comments",
    )
    parser.add_argument("-c", "--numcomments", help="The number of comments to fetch")
    parser.add_argument(
        "-n",
        "--numsubmissions",
        help="The number of submissions to fetch from the subreddit",
    )

    args = parser.parse_args()
    return args

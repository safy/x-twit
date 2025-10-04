from dataclasses import dataclass
from datetime import datetime
from typing import List

import pytz
import snscrape.modules.twitter as sntwitter


@dataclass
class Tweet:
    content: str
    username: str
    displayname: str
    date: datetime
    like_count: int
    retweet_count: int
    reply_count: int
    url: str


def search_tweets(query: str, limit: int = 50) -> List[Tweet]:
    scraper = sntwitter.TwitterSearchScraper(query)
    tweets: List[Tweet] = []

    for tweet in scraper.get_items():
        if len(tweets) >= limit:
            break
        tweets.append(
            Tweet(
                content=tweet.rawContent,
                username=tweet.user.username,
                displayname=tweet.user.displayname,
                date=_to_utc(tweet.date),
                like_count=tweet.likeCount,
                retweet_count=tweet.retweetCount,
                reply_count=tweet.replyCount,
                url=f"https://x.com/{tweet.user.username}/status/{tweet.id}",
            )
        )

    return tweets


def _to_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=pytz.UTC)
    return value.astimezone(pytz.UTC)

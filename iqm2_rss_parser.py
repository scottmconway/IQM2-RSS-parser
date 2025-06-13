#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

IQM_DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"


def create_rss_feed(channel_info, items):
    """
    channel_info: dict with keys 'title', 'link', 'description', optionally 'language', 'author', etc.
    items: list of dicts, each with keys:
        'title', 'link', 'description', optionally 'pubDate' (datetime), 'guid', 'author'
    """

    fg = FeedGenerator()
    fg.title(channel_info.get("title", ""))
    fg.link(href=channel_info.get("link", ""), rel="alternate")
    fg.description(channel_info.get("description", ""))
    if "language" in channel_info:
        fg.language(channel_info["language"])
    if "author" in channel_info:
        fg.author({"name": channel_info["author"]})

    for itm in items:
        fe = fg.add_entry()
        fe.title(itm.get("title", ""))
        fe.link(href=itm.get("link", ""))
        fe.description(itm.get("description", ""))

        if "pubDate" in itm:
            pub = itm["pubDate"]
            fe.pubDate(pub)

        if "guid" in itm:
            fe.guid(itm["guid"])

        if "author" in itm:
            fe.author({"name": itm["author"]})

    return fg.rss_str()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "feed_url", type=str, help="The URL of the IQM2 feed to process"
    )
    feed_url = parser.parse_args().feed_url

    content = requests.get(
        feed_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        },
    ).text
    content = content.replace('<?xml version="1.0" encoding="utf-16"?>', "")
    soup = BeautifulSoup(content, "html.parser")

    feed_items = []

    divs = soup.body.find_all("div")
    feed_title = divs[0].h1.text
    feed_description = divs[0].h3.text

    channel = {
        "title": feed_title,
        "link": feed_url,
        "description": feed_description,
        "language": "en",
        "author": "",
    }
    for div in divs[1:]:
        written_time = div.em.text.split(":", 1)[1].strip()
        publish_date = datetime.strptime(written_time, IQM_DATETIME_FORMAT).astimezone(
            timezone.utc
        )

        feed_item = {
            "title": div.h2.text,
            "link": div.p.p.a.attrs["href"],
            "description": str(div),
            "pubDate": publish_date,
            "guid": div.p.p.a.attrs["href"],
            "author": "",
        }
        feed_items.append(feed_item)

    rss_bytes = create_rss_feed(channel, feed_items)
    print(rss_bytes.decode("utf-8"))


if __name__ == "__main__":
    main()

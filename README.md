# IQM2\_RSS\_parser

Sometime in 2025, IQM2 "updated" their RSS feeds to spit out _very broken_ HTML instead of a standard RSS feed. This script takes a feed URL as its sole argument and prints the proper feed contents to stdout. It works flawlessly with RSS readers such as [RSS Guard](https://github.com/martinrotter/rssguard).

_This script does not handle errors well, and is provided as a best-effort approach!_

# Requirements
* python3
* see requirements.txt

# Usage
`python3 iqm2_rss_parser.py "$FEED_URL"`

[Example feed URL](https://eastpointcityga.iqm2.com/Services/RSS.aspx?Feed=Calendar)

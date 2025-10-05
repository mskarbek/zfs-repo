#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = ["feedparser"]
# ///
import json

import feedparser

atom_url = "https://github.com/openzfs/zfs/releases.atom"
feed = feedparser.parse(atom_url)

with open("openzfs.json", "w") as file:
    file.write(
        json.dumps(
            {
                "version": feed["entries"][0]["title"],
                "url": f"https://github.com/openzfs/zfs/tags/download/{feed['entries'][0]['title']}/{feed['entries'][0]['title']}.tar.gz",
            }
        )
    )
    print(feed["entries"][0]["title"])

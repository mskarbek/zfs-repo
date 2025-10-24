#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = ["feedparser", "requests"]
# ///
import json
import re
from string import Template

import feedparser
import requests

atom_url = "https://github.com/openzfs/zfs/tags.atom"
feed = feedparser.parse(atom_url)

tag_meta_url = Template(
    "https://raw.githubusercontent.com/openzfs/zfs/refs/tags/${version}/META"
)
tag_dwonload_url = Template(
    "https://github.com/openzfs/zfs/archive/refs/tags/${version}.tar.gz"
)
master_meta_url = "https://raw.githubusercontent.com/openzfs/zfs/refs/heads/master/META"
master_dwonload_url = "https://github.com/openzfs/zfs/archive/refs/heads/master.tar.gz"

releases = {
    "2.2": {},
    "2.3": {},
    "2.4": {},
    "master": {},
}

regex = re.compile(r"Linux-Maximum: +([0-9]\.[0-9][0-9])")

for release in releases:
    with open(f"versions/openzfs-{release}.json", "w") as f:
        if release != "master":
            for entry in feed["entries"]:
                if (
                    f"zfs-{release}" in entry["title"]
                    and ".99" not in entry["title"]
                    and not releases[release]
                ):
                    version = entry["title"]
                    releases[release]["version"] = version[4:]
                    meta = requests.get(tag_meta_url.substitute({"version": version}))
                    kernel_max = regex.search(meta.text)
                    if kernel_max is not None:
                        releases[release]["max_kernel_version"] = kernel_max.group(1)
                    releases[release]["meta_url"] = tag_meta_url.substitute(
                        {"version": version}
                    )
                    releases[release]["dwonload_url"] = tag_dwonload_url.substitute(
                        {"version": version}
                    )
                    json.dump(releases[release], f, indent=2)
                    print(f"{version}")
        else:
            releases[release]["version"] = "master"
            meta = requests.get(master_meta_url)
            kernel_max = regex.search(meta.text)
            if kernel_max is not None:
                releases[release]["max_kernel_version"] = kernel_max.group(1)
            releases[release]["meta_url"] = master_meta_url
            releases[release]["dwonload_url"] = master_dwonload_url
            json.dump(releases[release], f, indent=2)
            print("master")

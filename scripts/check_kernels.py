#!/usr/bin/env -S uv run --script
#
# /// script
# dependencies = ["koji"]
# ///
import json

import koji

koji_config = [
    {
        "koji_url": "https://koji.fedoraproject.org/kojihub",
        "pkgs_url": "https://kojipkgs.fedoraproject.org",
        "tags": [
            "f41",
            "f41-updates",
            "f42",
            "f42-updates",
            "f43",
            "f43-updates",
            "eln",
            "rawhide",
        ],
    },
    {
        "koji_url": "https://kojihub.stream.centos.org/kojihub",
        "pkgs_url": "https://kojihub.stream.centos.org/kojifiles",
        "tags": [
            "c9s-released",
            "c9s-compose",
            "c9s-gate",
            "c9s-draft",
            "c10s-released",
            "c10s-compose",
            "c10s-gate",
            "c10s-draft",
        ],
    },
]

packages = [
    "kernel",
    "kernel-core",
    "kernel-devel",
    "kernel-headers",
    "kernel-abi-stablelists",
]

for config in koji_config:
    session = koji.ClientSession(f"{config['koji_url']}")
    for tag in config["tags"]:
        kernels = session.getLatestBuilds(tag, package="kernel")
        rpms = session.getLatestRPMS(tag, package="kernel")
        if rpms[1][0]["volume_name"] == "DEFAULT":
            url = f"{config['pkgs_url']}"
        else:
            url = f"{config['pkgs_url']}/vol/{rpms[1][0]['volume_name']}"
        with open(f"versions/{tag}.json", "w") as file:
            data = {}
            data["version"] = rpms[1][0]["version"]
            data["major_version"] = rpms[1][0]["version"].split(".")[0]
            data["minor_version"] = rpms[1][0]["version"].split(".")[1]
            data["release"] = rpms[1][0]["release"].rsplit(".", 1)[0]
            data["dist"] = rpms[1][0]["release"].rsplit(".", 1)[1]
            data["packages"] = []

            for rpm in rpms[0]:
                if rpm["arch"] == "x86_64" or rpm["arch"] == "noarch":
                    if rpm["name"] in packages:
                        data["packages"].append(
                            f"{url}/packages/kernel/{rpm['version']}/{rpm['release']}/{rpm['arch']}/{rpm['name']}-{rpm['version']}-{rpm['release']}.{rpm['arch']}.rpm"
                        )
            json.dump(data, file, indent=2, sort_keys=True)
            print(f"{tag}: {rpms[1][0]['version']}-{rpms[1][0]['release']}")

#!/bin/env python


def humanize_title(title: str) -> str:
    if title is None or title == "":
        return ""

    return " ".join([word.title() for word in title.split("_")])

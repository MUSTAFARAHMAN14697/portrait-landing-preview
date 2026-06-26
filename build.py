#!/usr/bin/env python3
"""Generate the Webflow-ready files from index.html (the readable source).

Outputs:
  index.webflow.html  - full document, comment-free + de-indented (single Embed)
  webflow.head.html   - inner <head> (loader, asset loader, GA, fonts) for
                        Webflow Page Settings -> Custom Code -> Head
  webflow.body.html   - inner <body> (markup + scripts) for an Embed element

All three are comment-stripped, de-indented, and blank-line-free.
"""
import re

src = open("index.html").read()

# strip HTML comments and /* */ block comments (CSS + JS), both multi-line safe
src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)


def clean(text):
    out = []
    for line in text.split("\n"):
        s = line.lstrip()
        if s == "" or s.startswith("//"):  # drop blanks + full-line // comments
            continue
        out.append(s)
    return "\n".join(out) + "\n"


# 1) full document
open("index.webflow.html", "w").write(clean(src))

# 2) inner <head>, minus charset/viewport (Webflow already provides those)
head_inner = re.search(r"<head>(.*?)</head>", src, flags=re.S).group(1)
head_inner = "\n".join(
    l for l in head_inner.split("\n")
    if "charset" not in l and 'name="viewport"' not in l
)
open("webflow.head.html", "w").write(clean(head_inner))

# 3) inner <body>
body_inner = re.search(r"<body[^>]*>(.*?)</body>", src, flags=re.S).group(1)
open("webflow.body.html", "w").write(clean(body_inner))

print("Generated: index.webflow.html, webflow.head.html, webflow.body.html")

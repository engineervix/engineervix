import re
import sys
import urllib.request

import feedparser

RSS_URL = "https://blog.victor.co.zm/rss.xml"
README_PATH = "README.md"
MAX_POSTS = 5
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def fetch_posts():
    req = urllib.request.Request(
        RSS_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        content = response.read()

    # Debug: show first 200 bytes so we can tell if it's XML or HTML
    preview = content[:200].decode("utf-8", errors="replace")
    print(f"Feed preview: {preview}")

    feed = feedparser.parse(content)

    if not feed.entries:
        print(f"No entries found. bozo={feed.bozo}, exception={feed.get('bozo_exception')}")
        return []

    posts = []
    for entry in feed.entries[:MAX_POSTS]:
        title = entry.get("title", "Untitled")
        link = entry.get("link", "")
        posts.append(f"- [{title}]({link})")

    return posts


def update_readme(posts):
    with open(README_PATH, "r") as f:
        content = f.read()

    post_list = "\n".join(posts)
    new_content = re.sub(
        r"<!-- BLOG-POST-LIST:START -->.*?<!-- BLOG-POST-LIST:END -->",
        f"<!-- BLOG-POST-LIST:START -->\n{post_list}\n<!-- BLOG-POST-LIST:END -->",
        content,
        flags=re.DOTALL,
    )

    with open(README_PATH, "w") as f:
        f.write(new_content)


if __name__ == "__main__":
    posts = fetch_posts()
    if not posts:
        print("No posts found — skipping README update.")
        sys.exit(1)
    update_readme(posts)
    print(f"Updated README with {len(posts)} posts.")

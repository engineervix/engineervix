import json
import re
import sys
import urllib.request
from datetime import datetime

README_PATH = "README.md"
MAX_POSTS = 5
HASHNODE_API = "https://gql.hashnode.com"
BLOG_HOST = "blog.victor.co.zm"

QUERY = """
query PostsByPublication {
  publication(host: "%s") {
    posts(first: %d) {
      edges {
        node {
          title
          url
          publishedAt
        }
      }
    }
  }
}
""" % (BLOG_HOST, MAX_POSTS)


def fetch_posts():
    payload = json.dumps({"query": QUERY}).encode()
    req = urllib.request.Request(
        HASHNODE_API,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        data = json.loads(response.read())

    edges = data.get("data", {}).get("publication", {}).get("posts", {}).get("edges", [])
    if not edges:
        print(f"No posts found in response: {data}")
        return []

    posts = []
    for edge in edges:
        node = edge.get("node", {})
        title = node.get("title", "Untitled")
        url = node.get("url", "")
        published = node.get("publishedAt", "")
        if published:
            date = datetime.fromisoformat(published.replace("Z", "+00:00")).strftime("%b %d, %Y")
            posts.append(f"- [{title}]({url}) — {date}")
        else:
            posts.append(f"- [{title}]({url})")

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

import json
import requests

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_ID = 34  # TDS KB


def fetch_all_topics():
    page = 0
    all_topics = []

    while True:
        url = f"{BASE_URL}/c/courses/tds-kb/{CATEGORY_ID}.json?page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            break

        data = response.json()
        topic_list = data.get("topic_list", {}).get("topics", [])

        if not topic_list:
            break

        all_topics.extend(topic_list)
        page += 1

    return all_topics


def fetch_topic_posts(topic_id):
    url = f"{BASE_URL}/t/{topic_id}.json"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    posts = data.get("post_stream", {}).get("posts", [])
    return posts


def fetch_posts_between(start, end):
    results = []
    all_topics = fetch_all_topics()

    for topic in all_topics:
        topic_id = topic["id"]

        # Only fetch posts within given range
        if not (start <= topic_id <= end):
            continue

        posts = fetch_topic_posts(topic_id)

        if not posts:
            continue

        results.append({
            "title": topic["title"],
            "id": topic["id"],
            "url": f"{BASE_URL}/t/{topic['id']}",
            "posts": posts
        })

    with open("scraper/discourse_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("✅ Saved scraped data to scraper/discourse_data.json")


# Example usage
if __name__ == "__main__":
    start = 1
    end = 999999  # You can adjust the range
    fetch_posts_between(start, end)

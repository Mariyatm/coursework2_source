import json
import os


def is_tag(word):
    return word.startswith("#")


def get_tag(word):
    return word.replace("#", "").replace("!", "")


def read_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    if path == os.path.join("data", "data.json"):
        for post in data:
            post["content"] = get_ref_content(post["content"])
    return data


def get_tag_as_href(tag):
    return f'<a href="/search?s={get_tag(tag)}">{ tag }</a>'


def get_ref_content(content):
    res_content = []
    for word in content.split():
        if is_tag(word):
            res_content.append(get_tag_as_href(word))
        else:
            res_content.append(word)
    return " ".join(res_content)


def get_posts_by_pattern(pattern):
    posts = read_json(os.path.join("data", "data.json"))
    pattern_posts = []
    for post in posts:
        if pattern in post["content"]:
            pattern_posts.append(post)
    pattern_posts = get_comment_posts(pattern_posts)
    return pattern_posts


def get_comment_posts(posts):
    comments = read_json(os.path.join("data", "comments.json"))
    for post in posts:
        len_comments = len([comment for comment in comments if comment["post_id"] == post["pk"]])
        post["len_com"] = len_comments
        post["content"] = post["content"][0:60] + "..."
    return posts


def get_post(post_id):
    posts = read_json(os.path.join("data", "data.json"))
    post = False
    for p in posts:
        if p["pk"] == post_id:
            post = p
    return post


def get_comments_for_post(post_id):
    comments = read_json(os.path.join("data", "comments.json"))
    post = get_post(post_id)
    if not post:
        return False
    comments_for_post = []
    for comment in comments:
        if comment["post_id"] == post["pk"]:
            comments_for_post.append(comment)
    return comments_for_post


def get_posts_by_user(user_name):
    posts = read_json(os.path.join("data", "data.json"))
    user_posts = []
    for post in posts:
        if post["poster_name"] == user_name:
            user_posts.append(post)
    return get_comment_posts(user_posts)


def add_comment(comment):
    print("!")
    comments = read_json(os.path.join("data", "comments.json"))
    with open(os.path.join("data", "comments.json"), "w") as f:
        comments.append(comment)
        json.dump(comments, f, ensure_ascii=False, indent=4)

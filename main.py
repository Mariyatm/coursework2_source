from flask import Flask, request, render_template, send_from_directory, jsonify
from pathlib import Path
import os, json
from functions import *

POST_PATH = "posts.json"
UPLOAD_FOLDER = os.path.join("uploads", "images")
app = Flask(__name__, static_folder="css")


@app.route('/')
def index():
    posts = read_json(os.path.join("data", "data.json"))
    posts = get_comment_posts(posts)
    return render_template('index.html', posts=posts)


@app.route('/posts/<int:post_id>', methods=['GET','POST'])
def post(post_id):
    post = get_post(post_id)
    comments = get_comments_for_post(post_id)
    if request.method == "POST":
        print("?")
        user, comment = request.form.get("user"), request.form.get("comment")
        add_comment({"post_id": post["pk"], "commenter_name": user, "comment": comment, "pk": len(comments)+1})
    comments = get_comments_for_post(post_id)
    return render_template('post.html', post=post, comments=comments)


@app.route('/search', methods=['GET'])
def search():
    pattern = request.args.get("s")
    if not pattern:
        pattern = ""
    posts = get_posts_by_pattern(pattern)
    return render_template('search.html', pattern=pattern, posts=posts)


@app.route('/users/<string:username>')
def users(username):
    posts = get_posts_by_user(username)
    return render_template('user-feed.html', posts=posts)


# @app.route("/bookmarks>")
# def bookmarks():
#     posts = read_json(os.path.join("data", "data.json"))
#     posts = get_comment_posts(posts)
#     return render_template('bookmarks.html', posts=posts)


@app.route("/img/<path:path>")
def static_dir(path):
    return send_from_directory("img", path)


if __name__ == "__main__":
    app.run()

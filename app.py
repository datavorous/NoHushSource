import os
import json
import random
import string
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load posts from the JSON file
with open('data/posts.json', 'r') as f:
    posts = json.load(f)

# Enable/disable Turnstile (set to False for local development)
ENABLE_TURNSTILE = True

# Topic names
topics = ['general', 'news', 'technology', 'sports', 'politics']

# Generate a random user ID
def generate_user_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Generate a random message ID
def generate_message_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

@app.route('/')
def home():
    if 'user_id' not in session:
        session['user_id'] = generate_user_id()
    return render_template('home.html', topics=topics)

@app.route('/topic/<topic_name>', methods=['GET', 'POST'])
def topic(topic_name):
    if topic_name not in topics:
        return redirect(url_for('home'))

    if request.method == 'POST':
        message = request.form['message']
        message_id = generate_message_id()
        posts.setdefault(topic_name, []).append({
            'message_id': message_id,
            'user_id': session['user_id'],
            'message': message,
            'comments': []
        })
        save_posts()

    return render_template('topic.html', topic_name=topic_name, posts=posts.get(topic_name, []), topics=topics)

@app.route('/post/<message_id>', methods=['GET', 'POST'])
def post(message_id):
    for topic, topic_posts in posts.items():
        for post in topic_posts:
            if post['message_id'] == message_id:
                if request.method == 'POST':
                    comment = request.form['comment']
                    post['comments'].append({
                        'user_id': session['user_id'],
                        'comment': comment
                    })
                    save_posts()
                return render_template('post.html', post=post)
    return redirect(url_for('home'))

def save_posts():
    with open('data/posts.json', 'w') as f:
        json.dump(posts, f)

if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(debug=True)

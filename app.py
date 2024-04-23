from flask import Flask, render_template, request, redirect, session, url_for
import json
import random
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['DISABLE_TURNSTILE'] = False # Add this line to disable Turnstile during local development

# Load posts from database
def load_posts():
    if os.path.exists('posts.json'):
        with open('posts.json', 'r') as f:
            data = json.load(f)
            return data.get('topics', [])
    else:
        return []

from uuid import uuid4  # Import uuid4 function to generate unique message IDs

@app.route('/new_post/<topic_name>', methods=['POST'])
def new_post(topic_name):
    message = request.form['message']
    user_id = session.get('user_id')
    if not user_id:
        user_id = generate_user_id()
        session['user_id'] = user_id

    # Generate a unique message_id
    message_id = str(uuid4())

    # Create the new post with the message_id
    post = {
        'user_id': user_id,
        'message': message,
        'date': datetime.now().strftime("%d/%m/%y %H:%M:%S"),
        'message_id': message_id  # Assign the generated message_id
    }

    # Save the new post
    save_post(topic_name, post)

    return redirect(url_for('topic', topic_name=topic_name))


# Save post to database
def save_post(topic_name, post):
    data = {'topics': load_posts()}
    topic = next((t for t in data['topics'] if t['name'] == topic_name), None)
    if topic is None:
        topic = {'name': topic_name, 'posts': []}
        data['topics'].append(topic)

    existing_post = next((p for p in topic['posts'] if p['message_id'] == post['message_id']), None)
    if existing_post:
        existing_post.update(post)
    else:
        post['message_id'] = generate_message_id()
        topic['posts'].append(post)

    with open('posts.json', 'w') as f:
        json.dump(data, f)

# Generate a message ID
def generate_message_id():
    return random.randint(10000, 999999)  # Adjust as needed for your requirements

@app.route('/')
def index():
    topics = load_posts()
    return render_template('index.html', topics=topics)

@app.route('/topic/<topic_name>')
def topic(topic_name):
    topics = load_posts()
    topic = next((t for t in topics if t['name'] == topic_name), None)
    if topic is None:
        return "Topic not found"
    posts = topic.get('posts', [])
    posts.sort(key=lambda x: x['date'], reverse=True)
    message_id = generate_message_id()
    return render_template('home.html', posts=posts, message_id=message_id, topic_name=topic_name)

@app.route('/post/<message_id>', methods=['GET', 'POST'])
def post(message_id):
    posts = load_posts()
    for topic in posts:
        for post in topic.get('posts', []):
            if post.get('message_id') == int(message_id):
                if request.method == 'POST':
                    comment = request.form['comment']
                    user_id = session.get('user_id')
                    if not user_id:
                        user_id = generate_user_id()
                        session['user_id'] = user_id
                    post.setdefault('comments', []).append({
                        'user_id': user_id,
                        'comment': comment,
                        'date': datetime.now().strftime("%d/%m/%y %H:%M:%S")
                    })
                    save_post(topic['name'], post)
                return render_template('message.html', post=post)
    return "Message not found"

@app.route('/message/<int:message_id>')
def display_message(message_id):
    posts = load_posts()
    for topic in posts:
        for post in topic.get('posts', []):
            if post.get('message_id') == message_id:
                return render_template('message.html', post=post)
    return "Message not found"

def generate_user_id():
    return random.randint(1000, 99999)

if __name__ == '__main__':
    app.run(debug=True)
